from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .models import ArchivoMultimedia, HistorialCalculadora
import pymongo

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db_mongo = client["calculadora_db"]
archivos_mongo_collection = db_mongo["archivos_multimedia"]

def index(request):
    resultado = None
    num1 = None
    num2 = None

    if request.method == 'POST':
        # CASO 1: Calcular y guardar resultado
        if 'calcular' in request.POST:
            num1 = float(request.POST.get('num1'))
            num2 = float(request.POST.get('num2'))
            db_choice = request.POST.get('db_choice', 'default')
            resultado = num1 + num2

            HistorialCalculadora.objects.using(db_choice).create(
                num1=num1,
                num2=num2,
                resultado=resultado
            )

        # CASO 2: Subir archivo y guardar metadatos
        elif 'subir_archivo' in request.POST:
            titulo = request.POST.get('titulo')
            archivo = request.FILES.get('archivo')
            db_choice = request.POST.get('db_choice') # 'default', 'mysql_db', o 'mongo_db'

            if archivo and titulo:
                if db_choice in ['default', 'mysql_db']:
                    # Guardar usando el ORM de Django en PostgreSQL o MySQL
                    ArchivoMultimedia.objects.using(db_choice).create(
                        titulo=titulo,
                        archivo=archivo
                    )
                elif db_choice == 'mongo_db':
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

            return redirect('index')

    archivos_subidos = ArchivoMultimedia.objects.using('default').all()

    context = {
        'resultado': resultado,
        'num1': num1,
        'num2': num2,
        'archivos_subidos': archivos_subidos,
    }
    return render(request, 'calculadora/index.html', context)