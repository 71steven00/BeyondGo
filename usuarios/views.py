from django.shortcuts import render
from usuarios.decorators import rol_requerido
from django.core.mail import send_mail
import random
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.http import request
from django.urls import reverse, reverse_lazy
from django.conf import settings # importacion para enviar correos
from django.views.generic import DetailView, FormView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator #opcional de prueba
from .models import Usuario
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
# Importamos el formulario desde el módulo de usuarios
from usuarios.forms import RegistroClienteForm


# Create your views here.

# @rol_requerido('ADMIN_H')
# def panel_hotel(request):
#     return render(request, 'ruta/del/archivo.html') #Aca va el html de hoteles




# 1. Interfaz para Administrador General
@rol_requerido('ADMIN')
def dashboard_admin(request):
    # Retorna la plantilla HTML del panel general
    return render(request, 'admin_general/panel_control.html')


# 2. Interfaz para Administrador de Hotel
@rol_requerido('ADMIN', 'ADMIN_H')
def panel_hotel(request):
    # Retorna el HTML específico para gestionar el hotel
    return render(request, 'ruta/del/archivo.html')


# 3. Interfaz para Administrador de Restaurante
@rol_requerido('ADMIN','ADMIN_R')
def panel_restaurante(request):
    # Retorna el HTML específico para gestionar el restaurante
    return render(request, 'ruta/del/archivo.html')


# 4. Interfaz para Guía Turístico
@rol_requerido('ADMIN','GUIA')
def panel_guia(request):
    # Retorna la interfaz donde el guía ve sus tours asignados
    return render(request, 'ruta/del/archivo.html')


# 5. Interfaz para Cliente / Turista
@rol_requerido('TURISTA')
def inicio_turista(request):
    # Retorna el catálogo o inicio de búsquedas para turistas
    return render(request, 'ruta/del/archivo.html')




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
        if not user.is_authenticated:
            return reverse('login')
        # Superusuario o administrador general
        if user.is_superuser or user.rol == 'ADMIN':
            return reverse('dashboard_admin')
        elif user.rol == 'ADMIN_H':
            return reverse('panel_hotel')
        elif user.rol == 'ADMIN_R':
            return reverse('panel_restaurante')
        elif user.rol == 'GUIA':
            return reverse('panel_guia')
        return reverse('inicio')
        

    def form_valid(self, form):
        user = form.get_user() # obtenemos la instancia del usuario que intenta autenticarse
        
        #verificacion de seguridad: si la cuenta esta bloqueada o inactiva
        if user and not user.is_active:
            limpiar_mensajes_previos(self.request)
            messages.error(self.request, 'Tu cuenta ha sido bloqueada por superar el límite de intentos. Contacta al administrador.')
            return redirect('login')
        
        
        
        limpiar_mensajes_previos(self.request)
        auth_login(self.request, user) # Iniciar sesión formalmente (aquí se llena request.user)
        
        session_key = f'intentos_login_{user.pk}'
        self.request.session.pop(session_key, None)
        
        # Crear el mensaje de bienvenida para que se muestre tras la redirección
        nombre = getattr(user, 'nombre', None) or getattr(user, 'first_name', None) or user.username
        messages.success(self.request, f'Bienvenido, {nombre}.')

        # Redirigir a la URL correspondiente según el rol del usuario autenticado
        return HttpResponseRedirect(self.get_success_url())
    
    
    
    def form_invalid(self, form):
        email = form.cleaned_data.get('username') or self.request.POST.get('username')
        limpiar_mensajes_previos(self.request)

        user_obj = Usuario.objects.filter(email=email).first()

        # 1. Si el correo no existe en la BD
        if not user_obj:
            messages.error(self.request, 'El correo electrónico no coincide con ninguna cuenta.')
            return super().form_invalid(form)

        # 2. Si la cuenta ya está desactivada/bloqueada
        if not user_obj.is_active:
            messages.error(
                self.request,
                'Tu cuenta ha sido bloqueada por superar el límite de intentos. Contacta al administrador.'
            )
            return super().form_invalid(form)
        
        session_key = f'intentos_login_{user_obj.pk}'
        # Se usará una variable en sesión para contar las fallas del usuario actual
        intentos = self.request.session.get(session_key, 0) + 1
        self.request.session[session_key] = intentos
        self.request.session.modified = True

        max_intentos = getattr(settings, 'AXES_FAILURE_LIMIT', 3)
        intentos_restantes = max_intentos - intentos

        if intentos_restantes <= 0:
            user_obj.is_active = False
            user_obj.save()
            # Limpiamos el contador de la sesión
            self.request.session.pop(f'intentos_{user_obj.pk}', None)

            messages.error(
                self.request,
                'Has superado los 3 intentos permitidos. Tu cuenta ha sido bloqueada. Contacta al administrador.'
            )
        else:
            messages.error(
                self.request,
                f'Contraseña incorrecta. Te quedan {intentos_restantes} intento(s).'
            )

        return super().form_invalid(form)
    
    



@method_decorator(rol_requerido('ADMIN', 'ADMIN_H', 'ADMIN_R', 'GUIA', 'TURISTA'), name='dispatch')
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
            
            # generar codigo aleatorio de 6 digitos
            codigo = str(random.randint(10000, 999999))
            
            # Guardar el correo en sesión para los siguientes pasos
            self.request.session['email_recuperacion'] = email
            # Todo: Aquí generas y envías el código por correo (simulación por ahora: '123456')
            self.request.session['codigo_recuperacion'] = codigo
            asunto = 'Código de verificación - Recuperación de contraseña'
            mensaje = (
                f'Hola,\n\n'
                f'Hemos recibido una solicitud para restablecer tu contrasena en BeyondGo.\n\n'
                f'Tu codigo de verificación es: {codigo}\n\n'
                f'Si no realizaste esta solicitud, puedes ignorar este mensaje.'
            )

            try:
                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(self.request, 'Se ha enviado un código de verificación a tu correo.')
                return redirect('password_request') # Redirige a la vista de ingresar el código
                
            except Exception as e:
                print("ERROR AL ENVIAR CORREO:", e)
                messages.error(self.request, 'Ocurrió un error al enviar el correo. Por favor, intenta de nuevo.')
                return self.render_to_response(self.get_context_data())

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
        
        # Generar nuevo codigo aleatorio de 6 digitos
        if request.GET.get('resend') == 'true':
            nuevo_codigo =str(random.randint(100000, 999999))
            request.session['codigo_recuperacion'] = nuevo_codigo
        #Reenviar el correo con el nuevo codigo
            try:
                asunto = 'Codigo de verificacion - Reenvio de clave'
                mensaje = f'Tu nuevo codigo de verificacion es: {nuevo_codigo}'

                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Se ha reenviado un nuevo código de verificación a tu correo.')
                    
            except Exception as e:
                print("ERROR AL REENVIAR CORREO:", e)
                messages.error(request, f'Ocurrió un error al reenviar el correo: {e}')
            return redirect('password_request')
        return self.render_to_response(self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        """Maneja la verificación cuando el usuario escribe el código y presiona Enviar"""
        limpiar_mensajes_previos(self.request)

        codigo_ingresado = self.request.POST.get('codigo', '').strip()
        codigo_valido_en_sesion = self.request.session.get('codigo_recuperacion')

        # Validar que el código coincida con el guardado en sesión
        if not codigo_ingresado or codigo_ingresado != codigo_valido_en_sesion:
            messages.error(self.request, 'El código de verificación es incorrecto.')
            return self.render_to_response(self.get_context_data())

        messages.success(self.request, 'Código verificado correctamente.')
        return redirect('nueva_contraseña')
    

"""3. Ingresar nueva contraseña"""
class PasswordResetNewView(TemplateView):
    """Paso 3: Ingresar la nueva contraseña"""
    template_name = 'reset_password/nueva_contraseña.html'
    
    def get(self, request, *args, **kwargs):
        # Limpiar alertas anteriores si utilizas tu función auxiliar
        limpiar_mensajes_previos(request)

        # Validar si el usuario completó el paso previo de verificación
        if not request.session.get('email_recuperacion'):
            messages.error(request, 'Acceso no permitido. Por favor inicia el proceso de recuperación.')
            return redirect('password_reset')  # O la ruta que prefieras, ej. 'login'

        return super().get(request, *args, **kwargs)

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
