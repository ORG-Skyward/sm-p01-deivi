from datetime import datetime
import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .models import ArchivoMultimedia, HistorialCalculadora
import pymongo

# Conexión segura a MongoDB (protegida para evitar fallos en Render si no está disponible)
try:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
    db_mongo = client["calculadora_db"]
    archivos_mongo_collection = db_mongo["archivos_multimedia"]
except Exception:
    client = None
    archivos_mongo_collection = None

def index(request):
    resultado = None
    num1 = None
    num2 = None

    if request.method == 'POST':
        # CASO 1: Calcular y guardar resultado
        if 'calcular' in request.POST:
            try:
                num1 = float(request.POST.get('num1', 0))
                num2 = float(request.POST.get('num2', 0))
                db_choice = request.POST.get('db_choice', 'default')
                resultado = num1 + num2

                HistorialCalculadora.objects.using(db_choice).create(
                    num1=num1,
                    num2=num2,
                    resultado=resultado
                )
            except ValueError:
                resultado = "Error numérico"

        # CASO 2: Subir archivo y guardar metadatos
        elif 'subir_archivo' in request.POST:
            titulo = request.POST.get('titulo')
            archivo = request.FILES.get('archivo')
            db_choice = request.POST.get('db_choice', 'default') # 'default', 'mysql_db', o 'mongo_db'

            if archivo and titulo:
                if db_choice in ['default', 'mysql_db']:
                    # Guardar usando el ORM de Django en PostgreSQL (Neon) o MySQL
                    ArchivoMultimedia.objects.using(db_choice).create(
                        titulo=titulo,
                        archivo=archivo
                    )
                elif db_choice == 'mongo_db':
                    if archivos_mongo_collection is not None:
                        # Guardar físicamente en la carpeta media
                        fs = FileSystemStorage()
                        filename = fs.save(archivo.name, archivo)
                        file_url = fs.url(filename)

                        # Guardar metadatos en MongoDB
                        archivos_mongo_collection.insert_one({
                            "titulo": titulo,
                            "nombre_archivo": filename,
                            "ruta": file_url,
                            "fecha": datetime.now()
                        })
                    else:
                        # Advertencia o acción alternativa si Mongo no está activo en producción
                        pass

            return redirect('index')

    archivos_subidos = ArchivoMultimedia.objects.using('default').all()

    context = {
        'resultado': resultado,
        'num1': num1,
        'num2': num2,
        'archivos_subidos': archivos_subidos,
    }
    return render(request, 'calculadora/index.html', context)