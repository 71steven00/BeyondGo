from .views import hazte_miembro, pagina_inicio
from django.urls import path 

urlpatterns = [
    path('', pagina_inicio, name='inicio'),
    path('experiencias/', pagina_inicio, name='experiencias'),
    path('hospedaje/', pagina_inicio, name='hospedaje'),
    path('restaurantes/', pagina_inicio, name='restaurantes'),
    path('hazte_miembro/', hazte_miembro, name='hazte_miembro'),
    
]
