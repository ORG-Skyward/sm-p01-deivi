# src/main.py

def calcular_suma():
    # Definimos los números a sumar (pueden venir de variables, entradas o pruebas)
    num1 = 15
    num2 = 25
    
    # Realizamos la operación
    resultado = num1 + num2
    
    # Imprimimos el resultado con el formato que lee GitHub Actions
    print(f"El resultado de sumar {num1} + {num2} es: {resultado}")

if __name__ == "__main__":
    calcular_suma()