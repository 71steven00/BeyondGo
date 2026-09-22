
from app.urls import auth_views
from django.urls import path


urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name = 'inicio_sesion.html'), name = 'login'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='login/password_reset.html'), name='password_reset'),
]
