from django.urls import path
from .views import dashboard_super_admin, visualizar_template

urlpatterns = [
    path('', dashboard_super_admin, name='dashboard_admin'),
    path('gestion_usuarios', visualizar_template, name='gestion_usuarios'),
    
]