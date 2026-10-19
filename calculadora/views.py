from django.shortcuts import render, redirect
from .models import ArchivoMultimedia

def index(request):
    resultado = None
    num1 = request.POST.get('num1', '')
    num2 = request.POST.get('num2', '')

    if request.method == 'POST':
        # 1. Lógica de la Calculadora
        if 'num1' in request.POST and 'num2' in request.POST and 'calcular' in request.POST:
            try:
                resultado = float(num1) + float(num2)
            except ValueError:
                resultado = "Error de entrada"

        # 2. Lógica para subir archivos dinámicos a la carpeta media
        if 'subir_archivo' in request.POST and request.FILES.get('archivo'):
            titulo = request.POST.get('titulo', 'Sin título')
            archivo = request.FILES['archivo']
            ArchivoMultimedia.objects.create(titulo=titulo, archivo=archivo)
            return redirect('index')

    archivos_subidos = ArchivoMultimedia.objects.all().order_by('-fecha_subida')

    context = {
        'num1': num1,
        'num2': num2,
        'resultado': resultado,
        'archivos_subidos': archivos_subidos
    }
    return render(request, 'calculadora/index.html', context)