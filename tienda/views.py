from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from datetime import datetime
import os
import pymongo
from .models import PerfilVIP, ClienteGamer, CategoriaJuego, ProductoGaming, OrdenCompra, ItemOrden

# Conexión segura a MongoDB local para la tienda NoSQL
try:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
    db_mongo = client["tienda_gaming_db"]
    productos_mongo_collection = db_mongo["productos_nosql"]
except Exception:
    client = None
    productos_mongo_collection = None

def get_productos_hibridos():
    """Función auxiliar para unificar productos de Postgres/MySQL y etiquetar el servidor"""
    productos_default = list(ProductoGaming.objects.using('default').all())
    for p in productos_default:
        p.origen_db = "PostgreSQL (Local / Nube Neon)"

    productos_mysql = list(ProductoGaming.objects.using('mysql_db').all())
    for p in productos_mysql:
        p.origen_db = "MySQL Workbench"

    productos_nosql = []
    if productos_mongo_collection is not None:
        try:
            productos_nosql = list(productos_mongo_collection.find())
        except Exception:
            productos_nosql = []

    return productos_default + productos_mysql, productos_nosql

# --- 1. PANEL PRINCIPAL / DASHBOARD ---
def dashboard_view(request):
    prods_rel, prods_nosql = get_productos_hibridos()
    total_juegos = len(prods_rel) + len(prods_nosql)
    total_clientes = ClienteGamer.objects.using('default').count()
    total_ordenes = OrdenCompra.objects.using('default').count()

    context = {
        'total_juegos': total_juegos,
        'total_clientes': total_clientes,
        'total_ordenes': total_ordenes,
        'ultimas_ordenes': OrdenCompra.objects.using('default').all().order_by('-fecha_orden')[:5]
    }
    return render(request, 'tienda/dashboard.html', context)

# --- 2. MÓDULO CLIENTES (1:1) ---
def clientes_view(request):
    mensaje = None
    error = False
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre_cliente')
        gamertag = request.POST.get('gamertag')
        rango_vip = request.POST.get('rango_vip', 'Bronce')
        descuento = int(request.POST.get('descuento', 5))

        try:
            perfil = PerfilVIP.objects.using('default').create(rango=rango_vip, descuento_porcentaje=descuento)
            ClienteGamer.objects.using('default').create(nombre=nombre, gamertag=gamertag, perfil_vip=perfil)
            mensaje = f"Cliente '{gamertag}' registrado exitosamente con Perfil VIP."
        except IntegrityError:
            error = True
            mensaje = f"Error: El Gamertag o NIF/NIE '{gamertag}' ya se encuentra registrado en el sistema."

    context = {
        'clientes': ClienteGamer.objects.using('default').all(),
        'mensaje': mensaje,
        'error': error
    }
    return render(request, 'tienda/clientes.html', context)

# --- 3. MÓDULO CATÁLOGO & CATEGORÍAS (1:N) ---
def catalogo_view(request):
    mensaje = None
    if request.method == 'POST':
        if 'crear_categoria' in request.POST:
            cat_nombre = request.POST.get('nombre_categoria')
            CategoriaJuego.objects.get_or_create(nombre=cat_nombre)
            mensaje = f"Categoría '{cat_nombre}' creada con éxito."
        
        elif 'subir_videojuego' in request.POST:
            titulo = request.POST.get('titulo')
            precio = request.POST.get('precio')
            categoria_id = request.POST.get('categoria_id')
            archivo = request.FILES.get('archivo')
            tipo_entorno = request.POST.get('tipo_entorno')
            db_choice = request.POST.get('db_choice')

            if os.getenv("RENDER") or tipo_entorno == 'nube':
                db_choice = 'default'

            cat = CategoriaJuego.objects.get(id=categoria_id)

            if db_choice in ['default', 'mysql_db']:
                ProductoGaming.objects.using(db_choice).create(
                    nombre=titulo,
                    precio=precio or 0.00,
                    categoria=cat,
                    imagen=archivo
                )
                mensaje = f"Videojuego guardado en la base de datos ({db_choice})."
            elif db_choice == 'mongo_db' and productos_mongo_collection is not None:
                file_url = ""
                if archivo:
                    fs = FileSystemStorage()
                    filename = fs.save(archivo.name, archivo)
                    file_url = fs.url(filename)
                productos_mongo_collection.insert_one({
                    "titulo": titulo,
                    "precio": float(precio) if precio else 0.0,
                    "categoria": cat.nombre,
                    "ruta": file_url,
                    "fecha": datetime.now()
                })
                mensaje = "Videojuego guardado exitosamente en MongoDB NoSQL."
        return redirect('tienda_catalogo')

    prods_rel, prods_nosql = get_productos_hibridos()
    context = {
        'productos_relacionales': prods_rel,
        'productos_nosql': prods_nosql,
        'categorias': CategoriaJuego.objects.using('default').all(),
        'mensaje': mensaje
    }
    return render(request, 'tienda/catalogo.html', context)

# --- 4. MÓDULO ÓRDENES DE COMPRA (N:N HÍBRIDO) ---
def ordenes_view(request):
    mensaje = None
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        productos_seleccionados = request.POST.getlist('productos_seleccionados')

        if cliente_id and productos_seleccionados:
            cliente = ClienteGamer.objects.using('default').get(id=cliente_id)
            nueva_orden = OrdenCompra.objects.using('default').create(cliente=cliente)
            
            for item_str in productos_seleccionados:
                partes = item_str.split('|')
                if len(partes) == 3:
                    titulo, precio, origen = partes
                    ItemOrden.objects.using('default').create(
                        orden=nueva_orden,
                        titulo_juego=titulo,
                        precio=float(precio),
                        origen_db=origen
                    )

            mensaje = f"Orden de entrega #{nueva_orden.id} procesada con éxito con juegos de múltiples servidores."
        else:
            mensaje = "Error: Debe seleccionar un cliente y al menos un videojuego."
        
        return redirect('tienda_ordenes')

    prods_rel, prods_nosql = get_productos_hibridos()

    context = {
        'clientes': ClienteGamer.objects.using('default').all(),
        'productos_relacionales': prods_rel,
        'productos_nosql': prods_nosql,
        'ordenes': OrdenCompra.objects.using('default').all(),
        'mensaje': mensaje
    }
    return render(request, 'tienda/ordenes.html', context)

# --- 5. MÓDULO HISTORIAL DE SERVIDORES ---
def servidores_view(request):
    prods_rel, prods_nosql = get_productos_hibridos()
    context = {
        'productos_relacionales': prods_rel,
        'productos_nosql': prods_nosql,
    }
    return render(request, 'tienda/servidores.html', context)

# --- 6. MÓDULO DE MÉTRICAS Y TELEMETRÍA ---
def metricas_view(request):
    prods_rel, prods_nosql = get_productos_hibridos()
    total_relacionales = len(prods_rel)
    total_nosql = len(prods_nosql)
    total_general = total_relacionales + total_nosql
    
    context = {
        'total_general': total_general,
        'total_relacionales': total_relacionales,
        'total_nosql': total_nosql,
        'clientes_count': ClienteGamer.objects.using('default').count(),
        'ordenes_count': OrdenCompra.objects.using('default').count(),
    }
    return render(request, 'tienda/metricas.html', context)