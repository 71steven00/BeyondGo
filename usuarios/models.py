from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from datetime import date
from django.core.exceptions import ValidationError
from admin_panel.models import Servicio

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        
        if password:
            validate_password(password, user=self.model(email=email, **extra_fields))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'ADMIN')
        return self.create_user(email, password, **extra_fields) 
    
# 1. MODELO DE USUARIO PRINCIPAL
class Usuario(AbstractUser):
    # def __init__(self, *args, **kwargs):

    ROL_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('ADMIN_H', 'Administrador_hotel'),
        ('ADMIN_R', 'Administrador_Restaurante'),
        ('GUIA', 'Guia'),
        ('TURISTA', 'Turista'),
    )
    TIPO_DOCUMENTO_CHOICES = (
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
        ('PPT', 'Permiso de Permanecia Temporal'),
        ('RC', 'Registro Civil')
    )
    username= None
    solo_letras = RegexValidator(
        regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
        message='El campo solo debe contener letras y espacios.'
    )
    def validar_mayoria_edad(fecha_nacimiento):
        if fecha_nacimiento is None:
            return
        
        hoy = date.today()
        # Calcular edad exacta teniendo en cuenta el mes y el día
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        
        if edad < 18:
            raise ValidationError('Debes ser mayor de 18 años para registrarte.')
        
    first_name = models.CharField(max_length=50,blank=False, verbose_name="Nombre", validators=[solo_letras])
    telefono = PhoneNumberField(blank=False, region="CO")
    email = models.EmailField(max_length=254, unique= True, blank= False)
    rol = models.CharField(max_length=10,choices=ROL_CHOICES,default='TURISTA',verbose_name="Rol")
    tipo_documento = models.CharField(max_length=5, choices=TIPO_DOCUMENTO_CHOICES, default='CC', verbose_name='Tipo de documento')
    numero_documento = models.CharField(max_length=20, unique=True, null=True, blank=False, verbose_name='Número de documento')
    fecha_nacimiento = models.DateField(null=True, blank=False, verbose_name='Fecha de nacimiento', validators=[validar_mayoria_edad])
    
    # CONFIGURACIÓN PARA INICIO DE SESIÓN CON EMAIL
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'telefono']  # Solo los campos obligatorios al usar 'createsuperuser'
    
    objects = UsuarioManager()
    # Campos para el control de intentos fallidos de autentificacion.
    AXES_LOCKOUT_TEMPLATE = None
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_rol_display()})"
    
    
class Guia(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_guia',
        verbose_name='Cuenta de usuario'
    )
    certificado_turismo = models.ImageField(upload_to='certificados_guias/', blank=True, null=True, verbose_name="Certificado de Turismo")

    class Meta:
        verbose_name = 'Perfil Guía'
        verbose_name_plural = 'Perfiles Guías'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.usuario.rol = 'GUIA'
            self.usuario.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Guía: {self.usuario.first_name}"




# 3. ATRIBUTOS DE HOTEL / RESTAURANTE (ESTABLECIMIENTOS) - MODELO UNIFICADO
class Establecimiento(models.Model):
    TIPO_CHOICES = (
        ('Hotel', 'Hotel'),
        ('Restaurante', 'Restaurante'),
    )
    ESTADO_REVISION_CHOICES = (
        ('pendiente', 'Pendiente de revisión'),
        ('informacion', 'Información solicitada'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    )
  
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='establecimientos',
        verbose_name='Administrador del Establecimiento'
    )
    nombre = models.CharField(max_length=150, verbose_name='Nombre del Establecimiento')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Detalles')
    # Selector de tipo visible en el formulario
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='Hotel', verbose_name='Tipo de Establecimiento')
    direccion = models.CharField(max_length=200, verbose_name='Dirección') 
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad') 
    pais = models.CharField(max_length=100, blank=True, default='Colombia', verbose_name='País')  
    url_img = models.ImageField(upload_to='establecimientos/', blank=True, null=True, verbose_name='Imagen')
    rtn = models.FileField(upload_to='rtn/', max_length=255, blank=False, verbose_name='Registro Nacional de Turismo (RNT/RTN)')
    licencia_sanitaria = models.FileField(upload_to='licencias/', max_length=255, blank=False, null=True, verbose_name='Registro Sanitario')
    camara_comercio = models.FileField(upload_to='camara_comercio/', max_length=255, blank=False, verbose_name='Certificado de Cámara de Comercio')
    servicios = models.ManyToManyField(Servicio, blank=True, related_name="servicios_establecimiento", verbose_name="Servicios Ofrecidos")
    estado_revision = models.CharField(max_length=20, choices=ESTADO_REVISION_CHOICES, default='pendiente', verbose_name='Estado de revisión')
    observacion_revision = models.TextField(blank=True, verbose_name='Observación de revisión')
# Crea una columna en la base de datos de tipo verdadero/falso que por defecto será True (es decir, "Disponible" al crear un nuevo registro) y le asigna el nombre descriptivo "Estado Disponible" para el panel de administración.
    is_active = models.BooleanField(default=True, verbose_name="Disponible")
    # clase interna de configuración de Django Permite definir metadatos
    class Meta: 
        verbose_name = "Establecimiento"
        verbose_name_plural = "Establecimientos"

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"


