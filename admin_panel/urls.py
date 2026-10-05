from django.urls import path
from .views import dashboard_super_admin
from . import views
from .views import dashboard_super_admin, visualizar_template
urlpatterns = [
    path('', dashboard_super_admin, name='dashboard_admin'),
    path('solicitudes/', views.solicitudes_miembros, name='solicitudes_miembros'),
    path('gestion_usuarios', visualizar_template, name='gestion_usuarios'),
]