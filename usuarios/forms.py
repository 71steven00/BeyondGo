from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('email', 'first_name', 'telefono')
        labels = {
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'telefono': 'Teléfono de contacto',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@correo.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
        }