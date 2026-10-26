import os
from django.shortcuts import render, redirect
from django.db import connections
from django.db.utils import OperationalError
import pymongo
from .models import (
    ClienteGamer, 
    PerfilVIP, 
    CategoriaJuego, 
    ProductoGaming, 
    OrdenCompra, 
    ItemOrden
)

def get_productos_hibridos():
    """
    Obtiene y unifica los productos de PostgreSQL, MySQL y MongoDB (NoSQL)
    con un timeout rápido para evitar bloqueos en entornos cloud como Render.
    """
    productos_rel = []
    productos_nosql = []

    # 1. Obtener productos de PostgreSQL (Base de datos por defecto)
    try:
        productos_rel.extend(list(ProductoGaming.objects.using('default').all()))
    except Exception as e:
        print(f"[ERROR BD] PostgreSQL: {e}")

    # 2. Obtener productos de MySQL (Base de datos secundaria mysql_db)
    if 'mysql_db' in connections:
        try:
            productos_rel.extend(list(ProductoGaming.objects.using('mysql_db').all()))
        except Exception as e:
            print(f"[ERROR BD] MySQL Workbench: {e}")

    # 3. Obtener productos de MongoDB NoSQL (Protegido con timeout para producción)
    try:
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
        client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        
        db = client['glitch_game_db']
        for doc in db['productos'].find():
            raw_nombre = (
                doc.get('nombre') or 
                doc.get('titulo') or 
                doc.get('game_name') or 
                doc.get('name')
            )
            nombre_juego = raw_nombre if (raw_nombre and str(raw_nombre).strip()) else "Juego sin título (Mongo)"
            precio_juego = doc.get('precio') or doc.get('price') or 0.00
            
            # Recuperamos la ruta o nombre de la imagen guardada en Mongo
            ruta_imagen = doc.get('ruta') or doc.get('imagen', None)
            
            productos_nosql.append({
                'id': str(doc.get('_id')),
                'nombre': nombre_juego,
                'titulo': nombre_juego,
                'precio': float(precio_juego),
                'origen_db': doc.get('origen_db', 'MongoDB Local NoSQL'),
                'ruta': ruta_imagen,
                'imagen': ruta_imagen
            })
    except Exception as e:
        print(f"[AVISO BD] MongoDB no disponible en este entorno: {e}")

    return productos_rel, productos_nosql


def dashboard_view(request):
    """Vista principal del Dashboard del Admin Panel."""
    prods_rel, prods_nosql = get_productos_hibridos()
    total_juegos = len(prods_rel) + len(prods_nosql)
    ultimas_ordenes = OrdenCompra.objects.prefetch_related('items').order_by('-fecha_orden')[:5]
    for ord_obj in ultimas_ordenes:
        ord_obj.total_orden = sum(float(item.precio) for item in ord_obj.items.all())
    
    context = {
        'productos_relacionales': prods_rel,
        'productos_nosql': prods_nosql,
        'total_juegos': total_juegos,
        'total_clientes': ClienteGamer.objects.count(),
        'total_ordenes': OrdenCompra.objects.count(),
        'ultimas_ordenes': ultimas_ordenes,
    }
    return render(request, 'tienda/dashboard.html', context)


def clientes_view(request):
    """Vista para gestión y creación de Clientes Gamer y Perfiles VIP (Relación 1:1)."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre_cliente')
        gamertag = request.POST.get('gamertag')
        rango = request.POST.get('rango_vip', 'Bronce')
        
        if nombre and gamertag:
            cliente, created = ClienteGamer.objects.get_or_create(
                gamertag=gamertag,
                defaults={'nombre': nombre}
            )
            PerfilVIP.objects.update_or_create(
                cliente=cliente,
                defaults={'rango': rango}
            )
            print(f"[VERIFICACIÓN BD] Cliente VIP guardado: {gamertag} ({nombre})")
            return redirect(request.path)

    clientes = ClienteGamer.objects.all()
    context = {'clientes': clientes}
    return render(request, 'tienda/clientes.html', context)


def catalogo_view(request):
    """Vista del Catálogo Híbrido y creación en PostgreSQL, MySQL o MongoDB con soporte para 'archivo'."""
    if request.method == 'POST':
        if 'crear_categoria' in request.POST or request.POST.get('nombre_categoria'):
            nombre_cat = request.POST.get('nombre_categoria')
            if nombre_cat:
                cat, created = CategoriaJuego.objects.get_or_create(nombre=nombre_cat)
                print(f"[VERIFICACIÓN BD] Categoría creada/encontrada: {cat.nombre}")
                
        elif 'subir_videojuego' in request.POST or request.POST.get('titulo'):
            nombre = request.POST.get('titulo')
            precio = request.POST.get('precio')
            categoria_id = request.POST.get('categoria_id')
            db_choice = request.POST.get('db_choice', 'default')
            
            # Capturamos el archivo usando el nombre exacto del input HTML: 'archivo'
            imagen_file = request.FILES.get('archivo')
            
            if nombre and precio:
                # --- OPCIÓN A: MONGODB (NoSQL) ---
                if db_choice == 'mongo_db':
                    try:
                        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
                        client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
                        db = client['glitch_game_db']
                        
                        img_name = imagen_file.name if imagen_file else None
                        
                        db['productos'].insert_one({
                            "nombre": nombre,
                            "titulo": nombre,
                            "precio": float(precio),
                            "categoria_id": categoria_id,
                            "origen_db": "MongoDB Local NoSQL",
                            "ruta": img_name,
                            "imagen": img_name
                        })
                        print(f"[VERIFICACIÓN BD] 🚀 '{nombre}' guardado en MongoDB con archivo: {img_name}")
                    except Exception as e:
                        print(f"[ERROR MONGODB] {e}")

                # --- OPCIÓN B: MYSQL ---
                elif db_choice == 'mysql_db' and 'mysql_db' in connections:
                    try:
                        categoria = CategoriaJuego.objects.using('mysql_db').filter(id=categoria_id).first()
                        if not categoria:
                            categoria, _ = CategoriaJuego.objects.using('mysql_db').get_or_create(nombre="General")

                        kwargs = {
                            'nombre': nombre,
                            'precio': precio,
                            'categoria': categoria,
                            'origen_db': 'MySQL Workbench'
                        }
                        if imagen_file:
                            kwargs['imagen'] = imagen_file

                        ProductoGaming.objects.using('mysql_db').create(**kwargs)
                        print(f"[VERIFICACIÓN BD] 🚀 '{nombre}' guardado en MySQL Workbench.")
                    except Exception as ex:
                        print(f"[ERROR MYSQL] {ex}")

                # --- OPCIÓN C: POSTGRESQL (Default) ---
                else:
                    categoria = CategoriaJuego.objects.filter(id=categoria_id).first()
                    if not categoria:
                        categoria = CategoriaJuego.objects.first()
                        if not categoria:
                            categoria = CategoriaJuego.objects.create(nombre="General")
                    
                    kwargs = {
                        'nombre': nombre,
                        'precio': precio,
                        'categoria': categoria,
                        'origen_db': 'PostgreSQL'
                    }
                    if imagen_file:
                        kwargs['imagen'] = imagen_file

                    ProductoGaming.objects.using('default').create(**kwargs)
                    print(f"[VERIFICACIÓN BD] 🚀 '{nombre}' guardado en PostgreSQL.")

        return redirect(request.path)

    prods_rel, prods_nosql = get_productos_hibridos()
    categorias = CategoriaJuego.objects.all()
    
    context = {
        'productos_relacionales': prods_rel,
        'productos_nosql': prods_nosql,
        'categorias': categorias,
    }
    return render(request, 'tienda/catalogo.html', context)


def ordenes_view(request):
    """Vista de Órdenes de Compra utilizando los valores empaquetados del formulario HTML."""
    if request.method == 'POST':
        print(f"[DEBUG POST ORDEN]: {request.POST}")
        
        cliente_id = request.POST.get('cliente_id')
        cliente = None
        if cliente_id and cliente_id.isdigit():
            cliente = ClienteGamer.objects.filter(id=cliente_id).first()

        if cliente:
            orden = OrdenCompra.objects.create(cliente=cliente)
            productos_raw = request.POST.getlist('productos_seleccionados')
            
            items_creados = 0
            if productos_raw:
                for item_str in productos_raw:
                    partes = item_str.split('|')
                    if len(partes) == 3:
                        titulo = partes[0]
                        try:
                            precio = float(partes[1])
                        except ValueError:
                            precio = 0.00
                        origen = partes[2]
                        
                        ItemOrden.objects.create(
                            orden=orden,
                            titulo_juego=titulo,
                            precio=precio,
                            origen_db=origen
                        )
                        items_creados += 1
            
            if items_creados == 0:
                ItemOrden.objects.create(
                    orden=orden,
                    titulo_juego="Videojuego Asignado",
                    precio=0.00,
                    origen_db='Catálogo Global'
                )

            print(f"[VERIFICACIÓN BD] 🎉 Orden #{orden.id} creada para {cliente.gamertag} con {items_creados} ítems.")
        else:
            print(f"[ERROR ORDEN] No se encontró el cliente con el ID '{cliente_id}'.")

        return redirect(request.path)

    prods_rel, prods_nosql = get_productos_hibridos()
    ordenes = OrdenCompra.objects.prefetch_related('items').all()
    
    for ord_obj in ordenes:
        ord_obj.total_orden = sum(float(item.precio) for item in ord_obj.items.all())

    clientes = ClienteGamer.objects.all()
    
    context = {
        'ordenes': ordenes,
        'clientes': clientes,
        'productos_relacionales': prods_rel,
        'productos_nosql': prods_nosql,
    }
    return render(request, 'tienda/ordenes.html', context)


def servidores_view(request):
    """Vista del Estado de los Servidores de Base de Datos."""
    estado_postgres = True
    estado_mysql = False

    try:
        connections['default'].cursor()
    except Exception:
        estado_postgres = False

    if 'mysql_db' in connections:
        try:
            connections['mysql_db'].cursor()
            estado_mysql = True
        except Exception:
            estado_mysql = False

    context = {
        'estado_postgres': estado_postgres,
        'estado_mysql': estado_mysql,
    }
    return render(request, 'tienda/servidores.html', context)


def metricas_view(request):
    """Vista de Métricas y Analítica del Sistema."""
    prods_rel, prods_nosql = get_productos_hibridos()
    context = {
        'total_general': len(prods_rel) + len(prods_nosql),
        'total_relacionales': len(prods_rel),
        'total_nosql': len(prods_nosql),
        'clientes_count': ClienteGamer.objects.count(),
        'ordenes_count': OrdenCompra.objects.count(),
    }
    return render(request, 'tienda/metricas.html', context)