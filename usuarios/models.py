from django.contrib.auth.models import AbstractUser
from django.db import models
import phonenumber_field
from phonenumber_field.modelfields import PhoneNumberField


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
    first_name = models.CharField(max_length=50,blank=False,verbose_name="Nombre")
    telefono = PhoneNumberField(blank=False, region="CO")
    email = models.EmailField(max_length=254, unique= True, blank= False)
    rol = models.CharField(max_length=10,choices=ROL_CHOICES,default='TURISTA',verbose_name="Rol")

    # CONFIGURACIÓN PARA INICIO DE SESIÓN CON EMAIL
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'telefono']  # Solo los campos obligatorios al usar 'createsuperuser'
    



class Admin_hotel(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name= 'perfil_admin_hotel',
        verbose_name= 'Cuenta de Usuario'
    )
    descripcion = models.TextField(blank=True, null = True, verbose_name= 'Detalles')
    # direccion =
    # ciudad=
    # pais= 
    # url_img= 
    # servicios = 
    # rtn = 
    # registro_sanitario = 

    
    
        