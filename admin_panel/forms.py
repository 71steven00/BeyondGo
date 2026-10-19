from django import forms

from .models import Experiencia


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