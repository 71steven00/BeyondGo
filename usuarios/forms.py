from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Usuario

class RegistroClienteForm(forms.ModelForm):
    password = forms.CharField(min_length=8, max_length=14)
    confirmar_contrasena = forms.CharField()

    class Meta:
        model = Cliente
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
        if Cliente.objects.filter(numero_documento=numero_documento).exists():
            raise ValidationError('Este número de documento ya está registrado.')
        return numero_documento

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        if password and confirmar_contrasena and password != confirmar_contrasena:
            self.add_error('confirmar_contrasena', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_password(self.cleaned_data['password'])
        if commit:
            cliente.save()
        return cliente