from django.shortcuts import render

def index(request):
    resultado = None
    num1 = request.GET.get('num1', '')
    num2 = request.GET.get('num2', '')

    if num1 != '' and num2 != '':
        try:
            resultado = float(num1) + float(num2)
        except ValueError:
            resultado = "Error: Ingresa números válidos"

    return render(request, 'calculadora/index.html', {
        'num1': num1,
        'num2': num2,
        'resultado': resultado
    })