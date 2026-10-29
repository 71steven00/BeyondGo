from django import forms

from .models import Experiencia
from usuarios.models import Establecimiento
from usuarios.models import Usuario


class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['titulo', 'duracion', 'precio', 'tipo', 'estado', 'imagen']
        widgets = {
            'imagen': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*',
                'data-experience-image-input': 'true',
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500 transition shadow-sm',
                'placeholder': 'ej. Tour nocturno por el lago'
            }),
            'duracion': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500 transition shadow-sm',
                'placeholder': 'ej. 4h'
            }),
            'precio': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500 transition shadow-sm',
                'placeholder': 'ej. $85.000 COP'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-500 focus:outline-none focus:border-emerald-500 transition shadow-sm'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-500 focus:outline-none focus:border-emerald-500 transition shadow-sm'
            }),
        }
 # FORMULARIO DE ESTABLECIMIENTOS 
  # =====================================================================
    # CONFIGURACIÓN DE CAMPOS OBLIGATORIOS Y RESTRICCIÓN DE FORMATO (PDF)
    # =====================================================================
    # Se declaran RTN y Licencia Sanitaria fuera de Meta para sobrescribir 
    # el comportamiento por defecto del modelo (que suele permitir nulos). 
    # Al definirlos aquí, se asegura que sean obligatorios (required=True) 
    # y que el explorador/backend acepte exclusivamente archivos PDF (.pdf).
class EstablecimientoForm(forms.ModelForm):
    # Campo RTN: Forzado como obligatorio (required=True) y limitado estrictamente a archivos .pdf
    rtn = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'w-full font-sans text-xs text-slate-500 file:mr-2 file:py-2 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 cursor-pointer',
            'accept': '.pdf' # Filtro nativo del explorador para mostrar solo PDFs
        })
    )
    # Campo Licencia Sanitaria: Forzado como obligatorio (required=True) y limitado estrictamente a archivos .pdf
    licencia_sanitaria = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'w-full font-sans text-xs text-slate-500 file:mr-2 file:py-2 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 cursor-pointer',
            'accept': '.pdf' # Filtro nativo del explorador para mostrar solo PDFs
        })
    )
    # Campo usuario filtrado para mostrar exclusivamente a administradores de hotel y restaurante
    # Define el campo 'usuario' como un campo de selección de modelos (ModelChoiceField)
    usuario = forms.ModelChoiceField(
        
        # Filtra la consulta (queryset) a la base de datos para mostrar únicamente
        # a los usuarios cuyo rol sea administrador de hotel ('ADMIN_H') o de restaurante ('ADMIN_R'),
        # excluyendo a turistas y administradores generales, ordenándolos alfabéticamente por su nombre.
        queryset=Usuario.objects.filter(rol__in=['ADMIN_H', 'ADMIN_R']).order_by('first_name'),
        
        # Establece que este campo es obligatorio para poder guardar el formulario.
        required=True,
        
        # Define los atributos CSS y de diseño de Tailwind para que mantenga 
        # la misma estética y paleta de colores de los demás inputs del sistema.
        widget=forms.Select(attrs={
            'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-500 focus:outline-none focus:border-emerald-500 transition shadow-sm'
        }),
        
        # Texto por defecto que aparece seleccionado antes de que el administrador elija una opción.
        empty_label="- Seleccione un propietario -"
    )
    class Meta:
        model = Establecimiento  
        fields = ['url_img', 'nombre', 'descripcion', 'tipo', 'direccion', 'ciudad', 'pais', 'rtn', 'licencia_sanitaria', 'servicios','usuario']
        widgets = {
# Se usa FileInput oculto con el atributo personalizado para activar el script de previsualización idéntico al de experiencias
            'url_img': forms.FileInput(attrs={
                'class': 'hidden', 
                'accept': 'image/*',
                'data-experience-image-input': 'true', # Atributo requerido por el script existente
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500 transition shadow-sm', 'placeholder': 'ej. Hotel El Real o Restaurante Sabor'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500 transition shadow-sm resize-none', 'rows': '3', 'placeholder': 'Escribe detalles...'}),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-500 focus:outline-none focus:border-emerald-500 transition shadow-sm'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500 transition shadow-sm', 'placeholder': 'ej. Vía Aquitania Km 12'
            }),
            'ciudad': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500 transition shadow-sm', 'placeholder': 'ej. Aquitania'
            }),
            'pais': forms.TextInput(attrs={
                'class': 'w-full px-3.5 py-3 bg-white border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-emerald-500 transition shadow-sm'
            }),
            'servicios': forms.CheckboxSelectMultiple(attrs={
                'class': 'grid grid-cols-2 gap-2 text-xs text-slate-700 accent-emerald-500'
            }),
        }
        
#FORMULARIO RAPIDO PARA UNIR CON EL FORMULARIO DE ESTABLECIMIENTO PARA AGREGAR USUARIO:
