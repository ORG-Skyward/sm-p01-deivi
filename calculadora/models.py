from django.db import models

class ArchivoMultimedia(models.Model):
    titulo = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='archivos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo