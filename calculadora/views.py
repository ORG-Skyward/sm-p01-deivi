from django.shortcuts import render
from pymongo import MongoClient
from .models import HistorialCalculadora

# Configuración de MongoDB
client = MongoClient("mongodb://localhost:27017/")
db_mongo = client["calculadora_db"]
historial_mongo_collection = db_mongo["historial_operaciones"]

def index(request):  # <--- Cambia el nombre aquí a 'index'
    resultado = None
    num1 = None
    num2 = None
    
    if request.method == 'POST':
        if 'calcular' in request.POST:
            try:
                num1 = float(request.POST.get('num1'))
                num2 = float(request.POST.get('num2'))
                resultado = num1 + num2
                
                db_choice = request.POST.get('db_choice', 'default')
                
                if db_choice == 'mongo_db':
                    historial_mongo_collection.insert_one({
                        "num1": num1,
                        "num2": num2,
                        "resultado": resultado,
                        "base_datos": "MongoDB"
                    })
                else:
                    operacion = HistorialCalculadora(num1=num1, num2=num2, resultado=resultado)
                    operacion.save(using=db_choice)
                    
            except ValueError:
                resultado = "Error: Ingresa números válidos"

    context = {
        'resultado': resultado,
        'num1': num1,
        'num2': num2,
    }
    
    return render(request, 'calculadora/index.html', context)