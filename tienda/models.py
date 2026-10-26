from django.db import models

class PerfilVIP(models.Model):
    rango = models.CharField(max_length=50)
    descuento_porcentaje = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.rango} ({self.descuento_porcentaje}%)"

class ClienteGamer(models.Model):
    nombre = models.CharField(max_length=100)
    gamertag = models.CharField(max_length=100, unique=True)
    perfil_vip = models.OneToOneField(PerfilVIP, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.gamertag} - {self.nombre}"

class CategoriaJuego(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class ProductoGaming(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(CategoriaJuego, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='portadas/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class OrdenCompra(models.Model):
    fecha_orden = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(ClienteGamer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente.gamertag}"

class ItemOrden(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='items')
    titulo_juego = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    origen_db = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.titulo_juego} (${self.precio}) [{self.origen_db}]"