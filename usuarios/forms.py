from django.contrib.auth.password_validation import validate_password
from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario, Guia
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from phonenumber_field.widgets import RegionalPhoneNumberWidget


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-slate-200 rounded-xl text-xs focus:outline-none focus:border-emerald-500',
            'placeholder': '••••••••'
        }),
        required=False,
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
    certificado_turismo = forms.ImageField(
        required=False,
        label="Certificado de Turismo (Solo Guías)",
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-600 file:mr-4 file:py-1 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-emerald-50 file:text-emerald-700 hover:file:bg-emerald-100'
        })
    )  

    class Meta: 
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefono', 'rol', 'is_active']
        exclude = [
            'password',
            'last_login',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si se está editando un usuario existente, excluimos los campos de contraseña
        if self.instance and self.instance.pk:
            self.fields.pop('password', None)
            self.fields.pop('confirm_password', None)
            if hasattr(self.instance, 'perfil_guia') and self.instance.perfil_guia.certificado_turismo:
                self.fields['certificado_turismo'].initial = self.instance.perfil_guia.certificado_turismo

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password)
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        # Solo se validan contraseñas al crear un usuario nuevo
        if not self.instance.pk:
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")
            if not password:
                self.add_error('password', 'La contraseña es obligatoria para usuarios nuevos.')
            elif password != confirm_password:
                self.add_error('confirm_password', 'Las contraseñas no coinciden.')
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # Solo en creación se encripta la contraseña
        if not self.instance.pk:
            password = self.cleaned_data.get("password")
            if password:
                usuario.set_password(password)
            
        if commit:
            usuario.save()

        # Manejo unificado del perfil del Guía
        if usuario.rol == 'GUIA':
            certificado = self.cleaned_data.get('certificado_turismo')
            guia, _ = Guia.objects.get_or_create(usuario=usuario)
            if certificado:
                guia.certificado_turismo = certificado
                guia.save()

        return usuario

# Alias de compatibilidad
Editar_usuario = UsuarioForm

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
        if numero_documento is None:
            raise ValidationError('El campo no puede estar vacio')
            return numero_documento
        elif Usuario.objects.filter(numero_documento=numero_documento).exists():
            raise ValidationError('Este número de documento ya está registrado.')
        return numero_documento
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password)
        return password
    
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
    
#Formulario para los datos de ver perfil
class UsuarioFormPerfil(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # Para evitar renderizar la etiqueta <form> duplicada
        
        # Validación condicional: Si el usuario es guía, agregamos el campo dinámicamente
        if hasattr(self.instance, 'perfil_guia') or getattr(self.instance, 'rol', None) == 'GUIA':
            self.fields['certificado_turismo'] = forms.ImageField(
                required=False, 
                label="Certificado de Turismo"
            )
            
        # Inyectamos clases directas a los controles de Crispy
        self.helper.layout = Layout(
            Field('first_name', css_class='w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl !text-white focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:bg-white/15 transition-all'),
            Field('last_name', css_class='w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl !text-white focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:bg-white/15 transition-all'),
            Field('email', css_class='w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl !text-white focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:bg-white/15 transition-all'),
            Field('telefono'),
            Field('numero_documento', css_class='w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl !text-white focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:bg-white/15 transition-all'),
            Field('fecha_nacimiento', css_class='w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl !text-white focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:bg-white/15 transition-all'),
        )
        self.helper.label_class = '!text-gray-200 font-semibold'
        self.helper.asterisk_field_css_class = ''
        
        # Si el campo existe, lo añadimos al layout visual de Crispy
        if 'certificado_turismo' in self.fields:
            if self.instance.pk:
                try:
                    self.fields['certificado_turismo'].initial = self.instance.perfil_guia.certificado_turismo
                except Guia.DoesNotExist:
                    pass
            self.helper.layout.append(
                Field('certificado_turismo', css_class='w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl !text-white focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:bg-white/15 transition-all')
            )

    class Meta:
        model = Usuario
        fields = '__all__'
        exclude = [
            'password',
            'rol',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'last_login',
            'date_joined',
            'tipo_documento'
        ]
        widgets = {
            'telefono': RegionalPhoneNumberWidget(attrs={
                'class': 'w-full px-4 py-3 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:bg-white/15 transition-all'
            }),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if commit:
            usuario.save()

        # Si el usuario es guía, guardamos el certificado
        if usuario.rol == 'GUIA':
            certificado = self.cleaned_data.get('certificado_turismo')
            if certificado:
                guia, _ = Guia.objects.get_or_create(usuario=usuario)
                guia.certificado_turismo = certificado
                guia.save()
        return usuario
        
        
