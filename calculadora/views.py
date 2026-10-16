from django.shortcuts import render

def index(request):
    resultado = None
    num1 = ''
    num2 = ''
    
    if request.method == 'POST':
        try:
            # Capturamos los valores enviados desde el formulario
            num1 = request.POST.get('num1')
            num2 = request.POST.get('num2')
            
            # Realizamos la suma (convertimos a float o int)
            resultado = float(num1) + float(num2)
        except (ValueError, TypeError):
            resultado = "Por favor ingresa números válidos"

    contexto = {
        'resultado': resultado,
        'num1': num1,
        'num2': num2
    }
    return render(request, 'calculadora/index.html', contexto)