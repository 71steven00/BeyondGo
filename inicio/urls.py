from .views import visualizar_template_header
from django.urls import path 

urlpatterns = [
    path('', visualizar_template_header, name='inicio_sesion'),
]
