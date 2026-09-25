from django import views
from app.urls import auth_views
from . import views 
from login.views import CustomLoginView
from django.urls import path
from django.contrib.auth import views as auth_views



urlpatterns = [
    # Tu vista de login personalizada (o auth_views.LoginView si prefieres la nativa)
    path('', CustomLoginView.as_view(), name='login'),
    
    # Tus rutas existentes
    path('registro/', views.registro, name='registro'),
    path('password_reset/', views.PasswordResetEmailView.as_view(), name='password_reset'),
    path('password_request/', views.PasswordResetCodeView.as_view(), name='password_request'),
    path('password_new/', views.PasswordResetNewView.as_view(), name='nueva_contraseña'),
]
    
