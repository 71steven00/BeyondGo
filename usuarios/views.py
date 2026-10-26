from django.shortcuts import render, redirect
from usuarios.decorators import rol_requerido
import secrets  # Generador criptográficamente seguro para códigos de verificación (evita predicciones)
from django.utils import timezone  # Manejo de marcas de tiempo para expiración de códigos OTP
from django.contrib.auth.password_validation import validate_password  # Aplica los validadores configurados en settings
from django.core.exceptions import ValidationError  # Captura fallos de complejidad de contraseñas
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.http import request
from django.urls import reverse, reverse_lazy
from django.conf import settings # importacion para enviar correos
from django.views.generic import DetailView, FormView, TemplateView
from django.utils.decorators import method_decorator #opcional de prueba
from .models import Usuario
from django.contrib import messages
from django.contrib.auth.views import LoginView
# Importamos el formulario desde el módulo de usuarios
from usuarios.forms import RegistroClienteForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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


def axes_bloqueo_view(request, original_response=None, credentials=None):
    """
    Función llamada automáticamente por django-axes cuando una cuenta supera el límite de intentos.
    En lugar de arrojar una pantalla en blanco con texto plano (403), redirige al usuario a la
    pantalla de inicio de sesión con una alerta visual estilizada.
    """
    limpiar_mensajes_previos(request)
    messages.error(
        request,
        'Has superado el límite de 5 intentos fallidos. Por seguridad, el acceso para esta cuenta está bloqueado temporalmente durante 15 minutos.'
    )
    return redirect('login')


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
        user = form.get_user() # Obtenemos la instancia del usuario autenticado
        
        # Verificación de seguridad: si la cuenta fue desactivada administrativamente
        if user and not user.is_active:
            limpiar_mensajes_previos(self.request)
            messages.error(self.request, 'Tu cuenta está inactiva. Por favor, contacta al administrador.')
            return redirect('login')
        
        limpiar_mensajes_previos(self.request)
        auth_login(self.request, user) # Inicia la sesión formalmente
        
        # Crear el mensaje de bienvenida para que se muestre tras la redirección
        nombre = getattr(user, 'nombre', None) or getattr(user, 'first_name', None) or user.username
        messages.success(self.request, f'Bienvenido, {nombre}.')

        # Redirigir a la URL correspondiente según el rol del usuario autenticado
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        limpiar_mensajes_previos(self.request)

        # PREVENCIÓN DE ENUMERACIÓN DE USUARIOS:
        # Se muestra un mensaje neutro para no revelar si el correo existe o no en el sistema.
        # BLOQUEO CONTRA FUERZA BRUTA:
        # Se delega el bloqueo a django-axes en settings.py (por IP y usuario en base de datos),
        # evitando el bloqueo destructivo permanente de 'user.is_active = False'.
        messages.error(self.request, 'Correo electrónico o contraseña incorrectos.')
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
        email = self.request.POST.get('email', '').strip()
        limpiar_mensajes_previos(self.request)
    
        if not email:
            messages.error(self.request, 'Por favor, ingresa tu correo electrónico.')
            return self.render_to_response(self.get_context_data())

        # Validar si el correo existe en la base de datos
        if not Usuario.objects.filter(email=email).exists():
            messages.error(self.request, 'El correo electrónico no coincide con ninguna cuenta.')
            return self.render_to_response(self.get_context_data())
        
        # SEGURIDAD CRIPTOGRÁFICA (secrets):
        # Genera un código OTP de exactamente 6 dígitos usando el generador de entropía del sistema operativo.
        # Evita predecibilidad o debilidades de 'random.randint'.
        codigo = str(secrets.randbelow(900000) + 100000)
        
        # PERSISTENCIA TEMPORAL Y LÍMITES:
        # Guardamos en sesión el código junto con una marca de tiempo (timestamp) para controlar expiración (TTL).
        # Inicializamos el contador de intentos fallidos en 0 para evitar fuerza bruta contra el código.
        self.request.session['email_recuperacion'] = email
        self.request.session['codigo_recuperacion'] = codigo
        self.request.session['codigo_timestamp'] = timezone.now().timestamp()
        self.request.session['intentos_codigo'] = 0
        
        asunto = 'Código de verificación - Recuperación de contraseña'

        try:
            # Contexto que se inyectará en la plantilla HTML de correo
            contexto = {
                'codigo': codigo,
            }
            # Renderizar la plantilla HTML de correo
            html_contenido = render_to_string('emails/correo_recuperacion_contra.html', contexto)
            texto_plano = strip_tags(html_contenido)

            # Enviar correo multiparte seguro a través de SMTP
            email_msg = EmailMultiAlternatives(asunto, texto_plano, settings.DEFAULT_FROM_EMAIL, [email])
            email_msg.attach_alternative(html_contenido, "text/html")
            email_msg.send()

            messages.success(self.request, 'Se ha enviado un código de verificación a tu correo.')
            return redirect('password_request')
            
        except Exception as e:
            print("ERROR AL ENVIAR CORREO:", e)
            messages.error(self.request, 'Ocurrió un error al enviar el correo. Por favor, intenta de nuevo.')
            return self.render_to_response(self.get_context_data())


"""2. Verificar código"""
class PasswordResetCodeView(TemplateView):
    """Paso 2: Verificar o reenviar el código de 6 dígitos"""
    template_name = 'reset_password/codigo_verif.html'

    def get(self, request, *args, **kwargs):
        """Maneja el clic en 'Reenviar código'"""
        email = request.session.get('email_recuperacion')
    
        if not email:
            messages.error(request, 'No hay un proceso de recuperación activo. Inicia de nuevo.')
            return redirect('password_reset')
        
        # Generar nuevo código aleatorio seguro de 6 dígitos al presionar reenviar
        if request.GET.get('resend') == 'true':
            nuevo_codigo = str(secrets.randbelow(900000) + 100000)
            request.session['codigo_recuperacion'] = nuevo_codigo
            request.session['codigo_timestamp'] = timezone.now().timestamp()
            request.session['intentos_codigo'] = 0  # Reiniciar contador de intentos para el nuevo código
            
            asunto = 'Código de verificación - Reenvío de clave'

            try:
                # Contexto que se inyectará en la plantilla HTML
                contexto = {
                    'codigo': nuevo_codigo,
                }
                html_contenido = render_to_string('emails/correo_recuperacion_contra.html', contexto)
                texto_plano = strip_tags(html_contenido)
                # Enviar correo multiparte seguro a través de Gmail
                email_msg = EmailMultiAlternatives(asunto, texto_plano, settings.DEFAULT_FROM_EMAIL, [email])
                email_msg.attach_alternative(html_contenido, "text/html")
                email_msg.send()

                messages.success(request, 'Se ha reenviado un nuevo código de verificación a tu correo.')

            except Exception as e:
                print("ERROR AL REENVIAR CORREO:", e)
                messages.error(request, 'Ocurrió un error al reenviar el correo. Por favor, intenta de nuevo.')
                return redirect('password_reset')
            
        return self.render_to_response(self.get_context_data())
    
    def post(self, request, *args, **kwargs):
        """Maneja la verificación cuando el usuario escribe el código y presiona Enviar"""
        limpiar_mensajes_previos(self.request)

        email = self.request.session.get('email_recuperacion')
        codigo_valido_en_sesion = self.request.session.get('codigo_recuperacion')
        codigo_timestamp = self.request.session.get('codigo_timestamp')

        # 1. Validar que exista una sesión de recuperación activa
        if not email or not codigo_valido_en_sesion:
            messages.error(self.request, 'No hay un proceso de recuperación activo o ha expirado. Inicia de nuevo.')
            return redirect('password_reset')

        # 2. CONTROL DE CADUCIDAD (TTL de 15 minutos = 900 segundos):
        # Si el usuario tarda más de 15 minutos en ingresar el código, se anula para evitar el uso de códigos viejos.
        if codigo_timestamp and (timezone.now().timestamp() - codigo_timestamp > 900):
            self.request.session.pop('codigo_recuperacion', None)
            self.request.session.pop('email_recuperacion', None)
            self.request.session.pop('codigo_timestamp', None)
            self.request.session.pop('intentos_codigo', None)
            messages.error(self.request, 'El código ha expirado (límite de 15 minutos). Solicita uno nuevo.')
            return redirect('password_reset')

        # 3. CONTROL DE FUERZA BRUTA SOBRE EL CÓDIGO OTP:
        # Se limita a 5 intentos fallidos para impedir que un atacante adivine el código de 6 dígitos.
        intentos = self.request.session.get('intentos_codigo', 0) + 1
        self.request.session['intentos_codigo'] = intentos

        if intentos > 5:
            # Si supera los 5 intentos, destruimos los datos del código en la sesión por seguridad
            self.request.session.pop('codigo_recuperacion', None)
            self.request.session.pop('email_recuperacion', None)
            self.request.session.pop('codigo_timestamp', None)
            self.request.session.pop('intentos_codigo', None)
            messages.error(self.request, 'Superaste el límite de intentos permitidos para ingresar el código. Solicita uno nuevo.')
            return redirect('password_reset')

        codigo_ingresado = self.request.POST.get('codigo', '').strip()

        # 4. Validar coincidencia del código
        if not codigo_ingresado or codigo_ingresado != codigo_valido_en_sesion:
            intentos_restantes = 5 - intentos
            messages.error(self.request, f'El código de verificación es incorrecto. Te quedan {intentos_restantes} intento(s).')
            return self.render_to_response(self.get_context_data())

        # Código validado con éxito: autorizamos el paso 3 y limpiamos intentos
        self.request.session['reset_verified'] = True
        self.request.session.pop('intentos_codigo', None)
        
        messages.success(self.request, 'Código verificado correctamente.')
        return redirect('nueva_contraseña')


"""3. Ingresar nueva contraseña"""
class PasswordResetNewView(TemplateView):
    """Paso 3: Ingresar la nueva contraseña"""
    template_name = 'reset_password/nueva_contraseña.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Restringe el acceso si no se ha verificado el código previamente"""
        if not request.session.get('reset_verified'):
            messages.error(request, 'Debes verificar el código de recuperación antes de ingresar aquí.')
            return redirect('password_request')
        return super().dispatch(request, *args, **kwargs)

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
                # 3. VALIDACIÓN DE ROBUSTEZ Y SEGURIDAD:
                # Ejecuta los validadores configurados en settings.py (incluido PasswordRobustaValidator).
                # Evita que se introduzcan contraseñas inseguras (como admin123, 12345678 o menores a 8 caracteres).
                try:
                    validate_password(nueva_password, user=usuario)
                except ValidationError as e:
                    # Presenta los mensajes de error de los validadores al usuario en la interfaz
                    for error_msg in e.messages:
                        messages.error(self.request, error_msg)
                    return self.render_to_response(self.get_context_data())

                # 4. Asignación y encriptación segura mediante PBKDF2/Argon2 nativo de Django
                usuario.set_password(nueva_password)
                usuario.save()
                
                # 5. Limpieza de variables de sesión para cerrar el ciclo de recuperación
                self.request.session.pop('codigo_recuperacion', None)
                self.request.session.pop('email_recuperacion', None)
                self.request.session.pop('codigo_timestamp', None)
                self.request.session.pop('reset_verified', None)
                self.request.session.pop('intentos_codigo', None)
                
                messages.success(self.request, 'Contraseña actualizada con éxito. Ya puedes iniciar sesión.')
                return redirect('login')
                
        # Corrección de redirección: si ocurre un fallo o la sesión expiró, redirige a password_reset (no a una URL inexistente)
        messages.error(self.request, 'Ocurrió un error en el proceso o la sesión expiró. Inténtalo de nuevo.')
        return redirect('password_reset')


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
