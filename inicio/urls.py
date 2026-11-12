from .views import (
    detalle_experiencia,
    hazte_miembro,
    pagina_experiencias,
    pagina_inicio,
)
from django.urls import path 

urlpatterns = [
    path('', pagina_inicio, name='inicio'),
    path('experiencias/', pagina_experiencias, name='experiencias'),
    path('experiencias/<int:pk>/', detalle_experiencia, name='experiencia_detalle'),
    path('hospedaje/', pagina_inicio, name='hospedaje'),
    path('restaurantes/', pagina_inicio, name='restaurantes'),
    path('hazte_miembro/', hazte_miembro, name='hazte_miembro'),
    
]
