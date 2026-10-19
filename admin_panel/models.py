from django.db import models


# Create your models here.
class Experiencia(models.Model):
    TIPO_CHOICES = (
        ('Aventura', 'Aventura'),
        ('Cultura / Aventura', 'Cultura / Aventura'),
        ('Gastronomía', 'Gastronomía'),
        ('Relajación', 'Relajación'),
    )
    
    ESTADO_CHOICES = (
        ('Activo', 'Activo'),
        ('Pausado', 'Pausado'),
        ('Agotado', 'Agotado'),
    )

    titulo = models.CharField(max_length=150)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    duracion = models.CharField(max_length=50)
    precio = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    imagen = models.ImageField(upload_to='experiencias/', blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo