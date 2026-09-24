from django import views
from app.urls import auth_views
from django.urls import path
from . import views 

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name = 'inicio_sesion.html'), name = 'login'),
    path('registro/', views.registro, name='registro'),
    path('email/', views.email_request_view, name='email_request'),
    path('password-request/', views.codigo_verif_view, name='password_request'),
    path('password-reset/', views.nueva_contrasena_view, name='password_new'),
]
