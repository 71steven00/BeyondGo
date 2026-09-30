from django.contrib.auth import login as auth_login
from django.http import request
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.shortcuts import render
from django.views.generic import DetailView, FormView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from usuarios.models import Usuario
from django.contrib import messages
from django.contrib.auth.views import LoginView
from axes.models import AccessAttempt
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
# Importamos el formulario desde el módulo de usuarios
from usuarios.forms import RegistroClienteForm


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
            if user.is_authenticated and (user.is_superuser or user.is_staff):
                return reverse('dashboard_admin')
            # Para usuarios normales, redirige a la URL configurada por defecto
            return super().get_success_url()
        

    def form_valid(self, form):
            # limpiar mensajes de error o intentos previos al momento de iniciar sesion
            limpiar_mensajes_previos(self.request)
            
            auth_login(self.request, form.get_user())
            
            # 2. Iniciar sesión formalmente (aquí se llena request.user)
            user = form.get_user()
            auth_login(self.request, user)

            # 3. Crear el mensaje de bienvenida para que se muestre tras la redirección
            nombre = getattr(user, 'nombre', None) or getattr(user, 'first_name', None) or user.username
            messages.success(self.request, f'Bienvenido, {nombre}.')

            # 4. Redirigir a la URL correspondiente según el rol del usuario autenticado
            return redirect(self.get_success_url())
        
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

"""Parte de recuperación de contraseña"""
"""Logica de 3 pasos: 1. Solicitar correo """
class PasswordResetEmailView(TemplateView):
    # Paso 1: Solicitar correo electrónico
        template_name = 'reset_password/email_form.html'
        
        def post(self, request, *args, **kwargs):
            email = self.request.POST.get('email')
            limpiar_mensajes_previos(self.request)
        
        # Validar si el correo existe en la base de datos
            if not Usuario.objects.filter(email=email).exists():
                messages.error(self.request, 'El correo electrónico no coincide con ninguna cuenta.')
                return self.render_to_response(self.get_context_data())
            # Guardar el correo en sesión para los siguientes pasos
            self.request.session['email_recuperacion'] = email
        
            # TODO: Aquí generas y envías el código por correo (simulación por ahora: '123456')
            self.request.session['codigo_recuperacion'] = '123456'
        
            messages.success(self.request, 'Se ha enviado un código de verificación a tu correo.')
            return redirect('password_request')

"""2. Verificar código,"""
class PasswordResetCodeView(TemplateView):
        """Paso 2: Verificar o reenviar el código de 6 dígitos"""
        template_name = 'reset_password/codigo_verif.html'

        def get(self, request, *args, **kwargs):
            """Maneja el clic en 'Reenviar código'"""
            email = request.session.get('email_recuperacion')
        
            if not email:
                messages.error(request, 'No hay un proceso de recuperación activo. Inicia de nuevo.')
                return redirect('password_reset')
        
            limpiar_mensajes_previos(request)
        
        # Generar o actualizar el código de recuperación en sesión
            request.session['codigo_recuperacion'] = '123456'  # O tu lógica de código aleatorio
        
            messages.success(request, 'Se ha reenviado un nuevo código de verificación a tu correo.')
            return self.render_to_response(self.get_context_data())

        def post(self, request, *args, **kwargs):
            limpiar_mensajes_previos(self.request)
        
        # Captura directa del input oculto de 6 dígitos del HTML
            codigo_ingresado = self.request.POST.get('codigo', '').strip()
            codigo_valido_en_sesion = self.request.session.get('codigo_recuperacion')
        
            if not codigo_ingresado or codigo_ingresado != codigo_valido_en_sesion:
                messages.error(self.request, 'El código de verificación es incorrecto.')
                return self.render_to_response(self.get_context_data())
            
            messages.success(self.request, 'Código verificado correctamente.')
            return redirect('nueva_contraseña')

"""3. Ingresar nueva contraseña"""
class PasswordResetNewView(TemplateView):
    """Paso 3: Ingresar la nueva contraseña"""
    template_name = 'reset_password/nueva_contraseña.html'

    def post(self, request, *args, **kwargs):
        limpiar_mensajes_previos(self.request)
        nueva_password = self.request.POST.get('new_password')
        confirmar_password = self.request.POST.get('confirm_password')

        # 1. Validar que los campos obligatorios no estén vacíos
        if not nueva_password or not confirmar_password:
            messages.error(self.request, 'Por favor, completa todos los campos obligatorios.')
            return self.render_to_response(self.get_context_data())

        # 2. Validar que ambas contraseñas coincidan
        if nueva_password != confirmar_password:
            messages.error(self.request, 'Las contraseñas no coinciden.')
            return self.render_to_response(self.get_context_data())
            
        # Recuperar al usuario usando el correo guardado en sesión
        email = self.request.session.get('email_recuperacion')
        if email:
            usuario = Usuario.objects.filter(email=email).first()
            if usuario:
                usuario.set_password(nueva_password)
                usuario.save()
                
                # Limpiar variables temporales de la sesión
                self.request.session.pop('codigo_recuperacion', None)
                self.request.session.pop('email_recuperacion', None)
                
                messages.success(self.request, 'Contraseña actualizada con éxito. Ya puedes iniciar sesión.')
                return redirect('login')
                
        messages.error(self.request, 'Ocurrió un error en el proceso. Inténtalo de nuevo.')
        return redirect('email_request')


# validaciones de registro de usuario:

class CustomRegisterView(FormView):
    template_name = 'registro.html'
    form_class = RegistroClienteForm
    success_url = reverse_lazy('login')  # URL a la que redirige tras registrarse

    def form_valid(self, form):
        # 1. Limpiar mensajes previos en la sesión
        limpiar_mensajes_previos(self.request)

        # 2. Guardar el usuario/cliente en la base de datos
        form.save()

        # 3. Lanzar alerta de éxito
        messages.success(
            self.request,
            'Registro exitoso. Por favor, inicia sesión.'
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        # 1. Limpiar mensajes previos en la sesión
        limpiar_mensajes_previos(self.request)
        primer_error = 'Por favor, corrige los errores del formulario.'
        
        if form.errors:
            for field, errors in form.errors.items():
                if errors:
                    primer_error = errors[0]
                    break
        messages.error(self.request, primer_error)
        return super().form_invalid(form)
