from django.shortcuts import render

def index_calculadora(request):
    resultado = None
    num1 = None
    num2 = None
    
    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1', 0))
            num2 = float(request.POST.get('num2', 0))
            resultado = num1 + num2
        except ValueError:
            resultado = "Por favor ingresa números válidos"
            
    return render(request, 'calculadora/index.html', {
        'resultado': resultado,
        'num1': num1,
        'num2': num2
    })