from django.shortcuts import render, redirect, get_object_or_404
from django.db import connections
from django.db.utils import OperationalError
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
    Obtiene los productos de la base de datos principal (PostgreSQL)
    y gestiona la conexion a la base de datos secundaria (MySQL) 
    evitando que la app falle si MySQL no esta accesible en Render.
    """
    productos_rel = []
    productos_nosql = []

    # 1. Obtener productos de PostgreSQL (Base de datos por defecto)
    try:
        productos_rel = list(ProductoGaming.objects.using('default').all())
    except Exception as e:
        print(f"Error al consultar PostgreSQL: {e}")
        productos_rel = []

    # 2. Intentar obtener productos de MySQL (si esta configurada en settings.py)
    if 'mysql' in connections:
        try:
            productos_nosql = list(ProductoGaming.objects.using('mysql').all())
        except (OperationalError, Exception) as e:
            print(f"Aviso: Servidor MySQL no disponible en produccion ({e}). Usando lista de respaldo.")
            productos_nosql = []
    else:
        # Si no hay alias 'mysql' en DATABASES, mantenemos la lista vacia para evitar excepciones
        productos_nosql = []

    return productos_rel, productos_nosql

def dashboard_view(request):
    """Vista principal del Dashboard del Admin Panel."""
    prods_rel, prods_nosql = get_productos_hibridos()
    
    context = {
        'productos_rel': prods_rel,
        'productos_nosql': prods_nosql,
        'total_clientes': ClienteGamer.objects.count(),
        'total_ordenes': OrdenCompra.objects.count(),
    }
    return render(request, 'tienda/dashboard.html', context)


def clientes_view(request):
    """Vista para gestion de Clientes Gamer y Perfiles VIP."""
    clientes = ClienteGamer.objects.all()
    context = {'clientes': clientes}
    return render(request, 'tienda/clientes.html', context)


def catalogo_view(request):
    """Vista del Catalogo de Productos Hibrido."""
    prods_rel, prods_nosql = get_productos_hibridos()
    categorias = CategoriaJuego.objects.all()
    
    context = {
        'productos_rel': prods_rel,
        'productos_nosql': prods_nosql,
        'categorias': categorias,
    }
    return render(request, 'tienda/catalogo.html', context)


def ordenes_view(request):
    """Vista de Ordenes de Compra registradas."""
    ordenes = OrdenCompra.objects.prefetch_related('items').all()
    context = {'ordenes': ordenes}
    return render(request, 'tienda/ordenes.html', context)


def servidores_view(request):
    """Vista del Estado de los Servidores de Base de Datos."""
    # Verificacion del estado de las conexiones
    estado_postgres = True
    estado_mysql = False

    try:
        connections['default'].cursor()
    except Exception:
        estado_postgres = False

    if 'mysql' in connections:
        try:
            connections['mysql'].cursor()
            estado_mysql = True
        except Exception:
            estado_mysql = False

    context = {
        'estado_postgres': estado_postgres,
        'estado_mysql': estado_mysql,
    }
    return render(request, 'tienda/servidores.html', context)


def metricas_view(request):
    """Vista de Metricas y Analitica del Sistema."""
    context = {
        'total_productos': ProductoGaming.objects.count(),
        'total_ventas': ItemOrden.objects.count(),
    }
    return render(request, 'tienda/metricas.html', context)