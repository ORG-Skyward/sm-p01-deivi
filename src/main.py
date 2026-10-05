# src/main.py

def generar_pagina_interactiva():
    # Todo el código HTML, CSS y JavaScript de la calculadora está guardado aquí dentro de Python
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Interactiva - GestioCore</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .card {
            background: white;
            padding: 30px 40px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            text-align: center;
            width: 320px;
        }
        h2 { color: #4a5568; margin-bottom: 20px; }
        .input-group {
            margin-bottom: 15px;
            text-align: left;
        }
        label { display: block; font-size: 14px; color: #718096; margin-bottom: 5px; font-weight: 600; }
        input {
            width: 100%;
            padding: 10px;
            box-sizing: border-box;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            font-size: 16px;
        }
        button {
            background: #319795;
            color: white;
            border: none;
            padding: 12px;
            width: 100%;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 10px;
            transition: background 0.3s;
        }
        button:hover { background: #2c7a7b; }
        .result {
            font-size: 20px;
            color: #2b6cb0;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="card">
        <h2>Calculadora Dinámica</h2>
        
        <div class="input-group">
            <label for="num1">Primer Número:</label>
            <input type="number" id="num1" placeholder="Ej. 15">
        </div>
        
        <div class="input-group">
            <label for="num2">Segundo Número:</label>
            <input type="number" id="num2" placeholder="Ej. 25">
        </div>
        
        <button onclick="realizarSuma()">Calcular Suma</button>
        
        <div class="result" id="resultado">Resultado: --</div>
    </div>

    <script>
        function realizarSuma() {
            const val1 = parseFloat(document.getElementById('num1').value);
            const val2 = parseFloat(document.getElementById('num2').value);
            
            if (isNaN(val1) || isNaN(val2)) {
                document.getElementById('resultado').innerText = "Por favor ingresa ambos números";
                return;
            }
            
            const suma = val1 + val2;
            document.getElementById('resultado').innerText = `Resultado: ${suma}`;
        }
    </script>
</body>
</html>
"""
    
    # Python escribe este texto en un archivo index.html automáticamente
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("¡El archivo index.html con las cajas de texto y el botón se generó exitosamente desde Python!")

if __name__ == "__main__":
    generar_pagina_interactiva()