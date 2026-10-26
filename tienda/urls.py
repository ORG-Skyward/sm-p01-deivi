from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='tienda_dashboard'),
    path('clientes/', views.clientes_view, name='tienda_clientes'),
    path('catalogo/', views.catalogo_view, name='tienda_catalogo'),
    path('ordenes/', views.ordenes_view, name='tienda_ordenes'),
    path('servidores/', views.servidores_view, name='tienda_servidores'),
    path('metricas/', views.metricas_view, name='tienda_metricas'), # <--- Nueva ruta profesional
]