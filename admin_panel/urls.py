from django.urls import path
from .views import dashboard_super_admin
from . import views
from .views import dashboard_super_admin
urlpatterns = [
    path('', dashboard_super_admin, name='dashboard_admin'),
    path('solicitudes/', views.visualizar_template2, name='solicitudes_miembros'),
    path('gestion_usuarios/',views.gestion_usuarios , name='gestion_usuarios'),
    path('gestion_usuarios/<str:a>/', views.gestion_usuarios, name='gestion_usuarios_crear'),
    path('gestion_usuarios/<int:pk>/<str:a>/', views.gestion_usuarios, name='gestion_usuarios_accion'),
]
