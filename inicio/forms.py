from django import forms
from django.core.validators import FileExtensionValidator, RegexValidator
from phonenumber_field.formfields import PhoneNumberField

from usuarios.models import Establecimiento, Usuario


class SolicitudMiembroForm(forms.Form):
    nombre_establecimiento = forms.CharField(max_length=150)
    tipo_establecimiento = forms.ChoiceField(choices=Establecimiento.TIPO_CHOICES)
    nombre_propietario = forms.CharField(
        max_length=50,
        validators=[RegexValidator(regex=Usuario.solo_letras.regex, message='Ingresa un nombre válido.')],
    )
    email_contacto = forms.EmailField(max_length=254)
    telefono = PhoneNumberField(region='CO')
    direccion = forms.CharField(max_length=200)
    ciudad = forms.CharField(max_length=100)
    descripcion = forms.CharField(required=False, widget=forms.Textarea)
    rnt_file = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])],
    )
    sanidad_file = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])],
    )
    camara_comercio_file = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])],
    )

    def clean_email_contacto(self):
        email = self.cleaned_data['email_contacto'].strip()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta registrada con este correo.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        for field_name in ('rnt_file', 'sanidad_file', 'camara_comercio_file'):
            uploaded_file = cleaned_data.get(field_name)
            if uploaded_file and uploaded_file.size > 5 * 1024 * 1024:
                self.add_error(field_name, 'El archivo no puede superar los 5 MB.')
        return cleaned_data