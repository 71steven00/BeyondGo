from django.urls import path
from .views import dashboard_super_admin
from . import views

urlpatterns = [
    path('', dashboard_super_admin, name='dashboard_admin'),
    path('solicitudes/', views.solicitudes_miembros, name='solicitudes_miembros'),
]