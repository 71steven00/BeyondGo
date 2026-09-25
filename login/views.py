from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from usuarios.models import Usuario
from django.contrib import messages
from django.contrib.auth.views import LoginView
from axes.models import AccessAttempt

def limpiar_mensajes_previos(request):
    """Limpia los mensajes acumulados en la sesión antes de agregar uno nuevo."""
    storage = messages.get_messages(request)
    list(storage)  # Consume los mensajes de la sesión
    if hasattr(storage, '_queued_messages'):
        storage._queued_messages.clear(
        )  # Borra los mensajes añadidos en la petición actual
    
class CustomLoginView(LoginView):
  template_name = 'inicio_sesion.html'
  
  def get_success_url(self):
        user = self.request.user
        # Redirige al panel administrativo si es superusuario o miembro del staff
        if user.is_superuser or user.is_staff:
            return reverse('admin:index')

        # Para usuarios normales, redirige a la URL configurada por defecto
        return super().get_success_url()
  
  def form_invalid(self, form):
        # Capturar el correo ingresado en el campo username
        email = form.cleaned_data.get('username') or self.request.POST.get('username')
        
        limpiar_mensajes_previos(self.request)
        
        # 1. Validar si el correo no existe en la BD
        if not Usuario.objects.filter(email=email).exists():
            messages.error(self.request, 'El correo electrónico no coincide con ninguna cuenta.')
        else:
            # 2. Si existe, consultar los intentos en django-axes
            attempt = AccessAttempt.objects.filter(username=email).first()
            intentos_realizados = attempt.failures_since_start if attempt else 1
            max_intentos = getattr(settings, 'AXES_FAILURE_LIMIT', 3)
            intentos_restantes = max(0, max_intentos - intentos_realizados)
        
            if intentos_restantes <= 0:
                messages.error(
                    self.request,
                    'Has superado los 3 intentos permitidos. Tu cuenta ha sido bloqueada. Contacta al administrador.',
                )
            else:
                messages.error(
                    self.request,
                    f'Contraseña incorrecta.',
                )

        return super().form_invalid(form)
    
def lockout_respuesta_personalizada(request, credentials, *args, **kwargs):
  limpiar_mensajes_previos(request)

  email = ''
  if credentials and isinstance(credentials, dict):
    email = credentials.get('username') or credentials.get('email') or ''
  if not email:
    email = request.POST.get('username') or ''
  email = email.strip()

  # Validar si el correo existía en la base de datos
  if email and not Usuario.objects.filter(email__iexact=email).exists():
    messages.error(
        request, 'El correo electrónico no coincide con ninguna cuenta.'
    )
    return render(request, 'inicio_sesion.html', status=200)

  messages.error(
      request,
      'Has superado los 3 intentos permitidos. Tu cuenta ha sido bloqueada.'
      ' Contacta al administrador.',
  )
  return render(request, 'inicio_sesion.html', status=403)



@method_decorator(login_required, name='dispatch')
class PerfilUsuarioView(DetailView):
    model = Usuario
    template_name = 'login/perfil.html'
    context_object_name = 'usuario'

    def get_object(self):
        return self.request.user

def registro(request):
    return render(request, 'registro.html')