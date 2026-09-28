from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente

class RegistroClienteForm(forms.ModelForm):
    # 1. CAMPOS ADICIONALES DE CONTRASEÑA
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'form-control'
        }),
        min_length=8,
        max_length=14,
        label='Contraseña (8 a 14 caracteres)'
    )
    
    confirmar_contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'form-control'
        }),
        label='Confirmar contraseña'
    )

    # 2. METACLACE (CONFIGURACIÓN DEL MODELO)
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
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ej: Juan Esteban'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ej: Pérez Gómez'}),
            'tipo_documento': forms.Select(),
            'numero_documento': forms.TextInput(attrs={'placeholder': 'Ej: 1012345678'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': '3001234567'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    # 3. VALIDACIONES ESPECÍFICAS
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Cliente.objects.filter(email=email).exists():
            raise ValidationError('Este correo electrónico ya se encuentra registrado.')
        return email

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get('numero_documento')
        if Cliente.objects.filter(numero_documento=numero_documento).exists():
            raise ValidationError('Este número de documento ya está registrado.')
        return numero_documento

    # 4. VALIDACIÓN GENERAL (CRUZADA)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        if password and confirmar_contrasena:
            if password != confirmar_contrasena:
                self.add_error('confirmar_contrasena', 'Las contraseñas no coinciden.')

        return cleaned_data

    # 5. GUARDADO PERSONALIZADO EN LA BASE DE DATOS
    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_password(self.cleaned_data['password'])
        if commit:
            cliente.save()
        return cliente