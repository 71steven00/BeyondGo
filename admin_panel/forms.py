from django import forms

from .models import Experiencia
from usuarios.models import Establecimiento


class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['titulo', 'duracion', 'precio', 'tipo', 'estado', 'imagen']
        widgets = {
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

class EstablecimientoForm(forms.ModelForm):
    class Meta:
        model = Establecimiento  
        fields = ['url_img', 'nombre', 'descripcion', 'tipo', 'direccion', 'ciudad', 'pais', 'rtn', 'licencia_sanitaria', 'servicios']
        widgets = {
            'url_img': forms.ClearableFileInput(attrs={
                'class': 'hidden', 'accept': 'image/*'
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
            'rtn': forms.FileInput(attrs={
                'class': 'w-full text-xs text-slate-500 file:mr-2 file:py-2 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 cursor-pointer', 'accept': '.pdf,image/*'
            }),
            'licencia_sanitaria': forms.FileInput(attrs={
                'class': 'w-full text-xs text-slate-500 file:mr-2 file:py-2 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 cursor-pointer', 'accept': '.pdf,image/*'
            }),
            'servicios': forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2 text-xs text-slate-700'}),
        }