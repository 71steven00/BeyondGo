from login.views import PerfilUsuarioView
from django.urls import path
from .views import CustomLoginView



urlpatterns = [
    # Vista de perfil del usuario autenticado
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
]

