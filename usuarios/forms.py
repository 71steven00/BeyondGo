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
    
    
class Editar_usuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        
        exclude = [
            'tipo_documento',
            'numero_documento',
            'fecha_nacimiento',
            'password',          # Importante excluir la contraseña por seguridad
            'last_login',        # Campos del sistema heredados de AbstractUser
            'user_permissions',
            'groups',
            'is_superuser',
            'is_staff',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-700 focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-700 focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none',
                'placeholder': 'Apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-700 focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-700 focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none',
                'placeholder': '+573000000000'
            }),
            'rol': forms.Select(attrs={
                'class': 'w-full px-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-700 focus:bg-white focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 transition-all outline-none'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-emerald-600 bg-slate-100 border-slate-300 rounded focus:ring-emerald-500'
            }),
        }
        
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500',
            'placeholder': '••••••••'
        }),
        required=False, # Requerida solo al crear
        label="Contraseña"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500',
            'placeholder': '••••••••'
        }),
        required=False,
        label="Confirmar contraseña"
    )
    class Meta: 
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'rol', 'is_active']
        
        exclude = [
            'password',          # Importante excluir la contraseña por seguridad
            'last_login',        # Campos del sistema heredados de AbstractUser
            'user_permissions',
            'groups',
            'is_superuser',
            'is_staff',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500',
                'placeholder': 'Ej. Juan'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500',
                'placeholder': 'Ej. Pérez'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-slate-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500',
                'placeholder': '+57 300 000 0000'
            }),
            'rol': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-slate-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500 bg-white'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500'
            }),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Validación si se está creando un nuevo usuario (no hay instancia previa con ID)
        if not self.instance.pk:
            if not password:
                self.add_error('password', 'La contraseña es obligatoria para usuarios nuevos.')
            if password != confirm_password:
                self.add_error('confirm_password', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get("password")
        
        # Si se ingresó una contraseña, la encriptamos de forma segura
        if not usuario.username:
            usuario.username = self.cleaned_data.get("email")
            
        if password:
            usuario.set_password(password)
            
        if commit:
            usuario.save()
        return usuario