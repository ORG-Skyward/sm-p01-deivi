from django.db import models

# Modelo para guardar el historial de la calculadora (compatible con PostgreSQL y MySQL usando .using())
class HistorialCalculadora(models.Model):
    num1 = models.FloatField()
    num2 = models.FloatField()
    resultado = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.num1} + {self.num2} = {self.resultado}"


# Modelo para la sección de gestor de archivos multimedia
class ArchivoMultimedia(models.Model):
    titulo = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='archivos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo