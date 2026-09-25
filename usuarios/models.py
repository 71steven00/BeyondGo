from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
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
        ('TI', 'Tarjeta de Identidad'),
        ('RC', 'Registro Civil'),
        ('NU', 'Otro')
    )
    username= None
    first_name = models.CharField(max_length=50,blank=False,verbose_name="Nombre")
    telefono = PhoneNumberField(blank=False, region="CO")
    email = models.EmailField(max_length=254, unique= True, blank= False)
    rol = models.CharField(max_length=10,choices=ROL_CHOICES,default='TURISTA',verbose_name="Rol")

    # CONFIGURACIÓN PARA INICIO DE SESIÓN CON EMAIL
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'telefono']  # Solo los campos obligatorios al usar 'createsuperuser'
    
    objects = UsuarioManager()
    # Campos para el control de intentos fallidos de autentificacion.
    AXES_FAILURE_LIMIT = 5
    AXES_LOCKOUT_TEMPLATE = None



# 2. CATÁLOGO GLOBAL DE SERVICIOS (Reutilizable para Hoteles y Restaurantes)
class servicios(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Servicio")

    class Meta:
        verbose_name = "Servicios"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return self.nombre


# 3. PERFIL DE ADMINISTRADOR DE HOTEL
class hoteles(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name= 'perfil_admin_hotel',
        verbose_name= 'Cuenta de Usuario'
    )
    descripcion = models.TextField(blank=True, null = True, verbose_name= 'Detalles')
    direccion = models.CharField(max_length=200, verbose_name='Dirección') 
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad') 
    pais = models.CharField(max_length=100, default='Colombia', verbose_name='País')  
    url_img = models.ImageField(upload_to='hoteles/', blank=True, null=True, verbose_name='Imagen del Hotel')
    rtn = models.CharField(max_length=50, unique=True, verbose_name='Registro Nacional de Turismo (RNT/RTN)') 
    registro_sanitario = models.CharField(max_length=50, blank=True, null=True, verbose_name='Registro Sanitario')
    
    # servicios = esta en una clase aparte. Unión ManyToMany con el modelo Servicio
    servicios = models.ManyToManyField('servicios', blank=True, related_name="Hoteles", verbose_name="Servicios Ofrecidos")

    class Meta:
        verbose_name = "Administrador de Hotel"
        verbose_name_plural = "Administradores de Hoteles" 

    def __str__(self):
        return f"Hotel/Admin: {self.usuario.first_name}"


# 4. PERFIL DE ADMINISTRADOR DE RESTAURANTE
class restaurantes (models.Model):
    Usuario = models.OneToOneField(
        Usuario,
        on_delete = models.CASCADE,
        related_name = 'perfil_admin_restaurante',
        verbose_name = 'Cuenta de usuario'
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name= 'Detalles')
    direccion = models.CharField(max_length=200, verbose_name='Direccion')  
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')  
    pais = models.CharField(max_length=100, default='Colombia', verbose_name='Pais')     
    url_img = models.ImageField(upload_to='restaurantes/', blank=True, null=True, verbose_name='Imagen del Restaurante')

    # servicios = esta en una clase aparte. Unión ManyToMany con el modelo Servicio
    servicios = models.ManyToManyField('servicios', blank=True, related_name='Restaurantes', verbose_name='Servicios Ofrecidos')

    class Meta:
        verbose_name = 'Administrador de Restaurante'
        verbose_name_plural = 'Administradores de Restaurantes'

    def __str__(self):
        return f"Restaurante/Admin: {self.Usuario.first_name}"

class Admin(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_admin',
        verbose_name='Cuenta de usuario'
    )
    tipo_documento = models.CharField(max_length=5, choices=Usuario.TIPO_DOCUMENTO_CHOICES, default='CC', verbose_name='Tipo de documento')
    numero_documento = models.CharField(max_length=20, unique=True, blank=False, verbose_name='Número de documento')
    fecha_nacimiento = models.DateField(blank=False, null=False, verbose_name='Fecha de nacimiento')

    class Meta:
        verbose_name = 'Administrador general'
        verbose_name_plural = 'Administradores generales'

    def save(self, *args, **kwargs):
        # Asegura que al guardar el perfil, el rol del usuario base sea 'ADMIN'
        with transaction.atomic():
            self.usuario.rol = 'ADMIN'
            self.usuario.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Admin: {self.usuario.first_name} {self.usuario.last_name} ({self.numero_documento})"
    
class Cliente(Usuario):
    last_name = models.CharField(max_length=50, blank=False, verbose_name='Apellido')
    tipo_documento = models.CharField(max_length=5, choices=Usuario.TIPO_DOCUMENTO_CHOICES, default='CC', verbose_name='Tipo de documento')
    numero_documento = models.CharField(max_length=20, unique=True, blank=False, verbose_name='Numero de documento')
    fecha_nacimiento = models.DateField(blank=False, null=False, verbose_name='Fecha de nacimiento')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def save(self, *args, **kwargs):
        # Asigna automáticamente el rol 'TURISTA' al guardarse
        self.rol = 'TURISTA'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"TURISTA: {self.first_name} {self.last_name} {self.numero_documento}"

class Guia(Usuario):
    last_name = models.CharField(max_length=50, blank=False, verbose_name='Apellido')
    tipo_documento = models.CharField(max_length=5, choices=Usuario.TIPO_DOCUMENTO_CHOICES, default='CC', verbose_name='Tipo de documento')
    numero_documento = models.CharField(max_length=20, unique=True, blank=False, verbose_name='Numero de documento')
    fecha_nacimiento = models.DateField(blank=False, null=False, verbose_name='Fecha de nacimiento')
    certificado_turismo = models.ImageField(upload_to='certificados_guias/', blank=True, null=True, verbose_name="Certificado de Turismo")
    class Meta:
        verbose_name = 'Guia'
        verbose_name_plural = 'Guias'

    def save(self, *args, **kwargs):
        # Asigna automáticamente el rol 'TURISTA' al guardarse
        self.rol = 'GUIA'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"GUIA: {self.first_name} {self.last_name} {self.numero_documento}"

