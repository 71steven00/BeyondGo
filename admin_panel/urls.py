from django.urls import path

from . import views
from .views import dashboard_super_admin

urlpatterns = [
    path('', dashboard_super_admin, name='dashboard_admin'),
    path('gestion_usuarios/',views.gestion_usuarios , name='gestion_usuarios'),
    path('gestion_usuarios/<str:a>/', views.gestion_usuarios, name='gestion_usuarios_crear'),
    path('gestion_usuarios/<int:pk>/<str:a>/', views.gestion_usuarios, name='gestion_usuarios_accion'),
# Rutas de Gestión de Establecimientos (siguiendo exactamente la misma estructura)
    path('gestion_establecimientos/', views.gestion_establecimientos, name='gestion_establecimientos'),
    path('gestion_establecimientos/<str:a>/', views.gestion_establecimientos, name='gestion_establecimientos_crear'),
    path('gestion_establecimientos/<int:pk>/<str:a>/', views.gestion_establecimientos, name='gestion_establecimientos_accion'),
# Rutas de Gestión de Experiencias (siguiendo exactamente la misma estructura)
    path('gestion-experiencias/', views.experiencias, name='gestion_experiencias'),
    path('gestion-experiencias/<str:a>/', views.experiencias, name='gestion_experiencias_crear'),
    path('gestion-experiencias/<int:pk>/<str:a>/', views.experiencias, name='gestion_experiencias_accion'),
# Rutas de Gestión de Solicitudes (siguiendo exactamente la misma estructura)
    path('solicitudes/', views.gestion_solicitudes, name='solicitudes_miembros'),
]
