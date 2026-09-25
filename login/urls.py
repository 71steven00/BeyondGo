from login.views import CustomLoginView
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    # Tu vista de login personalizada (o auth_views.LoginView si prefieres la nativa)
    path('', CustomLoginView.as_view(), name='login'),
    
    # Tus rutas existentes
    path('registro/', views.registro, name='registro'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='login/password_reset.html'), name='password_reset'),
]