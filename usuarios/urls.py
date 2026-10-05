from django.urls import path
from . import views 

urlpatterns = [
    #URls del login:
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('registro/', views.CustomRegisterView.as_view(), name='registro'),
    path('password_reset/', views.PasswordResetEmailView.as_view(), name='password_reset'),
    path('password_request/', views.PasswordResetCodeView.as_view(), name='password_request'),
    path('password_new/', views.PasswordResetNewView.as_view(), name='nueva_contraseña'),
    
    # Vista de perfil del usuario autenticado
    path('perfil/', views.PerfilUsuarioView.as_view(), name='perfil'),
]

