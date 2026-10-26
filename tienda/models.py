from django.db import models

class ClienteGamer(models.Model):
    nombre = models.CharField(max_length=100)
    gamertag = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.gamertag

class PerfilVIP(models.Model):
    cliente = models.OneToOneField(ClienteGamer, on_delete=models.CASCADE, related_name='perfil_vip', null=True, blank=True)
    rango = models.CharField(max_length=50, default='Bronce')
    
    def __str__(self):
        return f"{self.cliente.gamertag if self.cliente else 'Sin cliente'} - {self.rango}"

class CategoriaJuego(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class ProductoGaming(models.Model):
    nombre = models.CharField(max_length=150)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(CategoriaJuego, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = "Producto Gaming"
        verbose_name_plural = "Productos Gaming"

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

class OrdenCompra(models.Model):
    cliente = models.ForeignKey(ClienteGamer, on_delete=models.CASCADE, related_name='ordenes')
    fecha_orden = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente.gamertag}"

class ItemOrden(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='items')
    titulo_juego = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    origen_db = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.titulo_juego} ({self.origen_db})"