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
    descripcion = models.TextField(blank=True, default='')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    duracion = models.CharField(max_length=50)
    precio = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    imagen = models.ImageField(upload_to='experiencias/', blank=True, null=True)
    incluye = models.TextField(blank=True, default='')
    ubicacion = models.TextField(blank=True, default='')
    visitas = models.PositiveIntegerField(default=0, editable=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    servicios = models.ManyToManyField('Servicio', blank=True, related_name='experiencias')
    def __str__(self):
        return self.titulo
    
    
class ExperienciaImagen(models.Model):
    experiencia = models.ForeignKey(
        Experiencia,
        on_delete=models.CASCADE,
        related_name='imagenes',
    )
    imagen = models.ImageField(upload_to='experiencias/galeria/')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Imagen de {self.experiencia.titulo}'


# 2. CATÁLOGO GLOBAL DE SERVICIOS (Reutilizable para Hoteles y Restaurantes)
class Servicio(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Servicio")
    descripcion = models.TextField(blank=True, default='', verbose_name="Descripción")

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre
    
