from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario

class RegistroClienteForm(forms.ModelForm):
    last_name = forms.CharField(
        max_length=150,
        required=True,
        error_messages={
            'required': 'Este campo es obligatorio.'
        }
    )
    
    password = forms.CharField(min_length=8, max_length=14)
    confirmar_contrasena = forms.CharField()

    class Meta:
        model = Usuario
        fields = [
            'first_name',
            'last_name',
            'tipo_documento',
            'numero_documento',
            'email',
            'telefono',
            'fecha_nacimiento',
        ]

    # Validaciones directas sobre los datos (sin mensajes de alerta)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email__iexact=email).exists():
            raise ValidationError('Este correo electrónico ya se encuentra registrado.')
        return email

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento')
        if Usuario.objects.filter(numero_documento=numero_documento).exists():
            raise ValidationError('Este número de documento ya está registrado.')
        return numero_documento

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        if password and confirmar_contrasena and password != confirmar_contrasena:
            self.add_error('confirmar_contrasena', 'Las contraseñas no coinciden.')
        elif not password or not confirmar_contrasena:
            if not password:
                self.add_error('password', 'la contraseña es requerida.')
            if not confirmar_contrasena:
                self.add_error('confirmar_contrasena', 'Debes confirmar la contraseña')
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        usuario.rol = 'TURISTA'
        
        if commit:
            usuario.save()
        return usuario