
from . import views

from app.urls import auth_views
from django.urls import path
urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name = 'inicio_sesion.html'), name = 'login'),
    path('registro/', views.registro, name='registro'),
    
]
