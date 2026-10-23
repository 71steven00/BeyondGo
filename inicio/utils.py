from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def enviar_correo_notificacion(destinatario_email, nombre_usuario, mensaje_personalizado, url=None):
    asunto = "Notificación importante - Aquitania BeyondGo"
    remitente = None  # Django usará automáticamente el DEFAULT_FROM_EMAIL del settings
    destinatarios = [destinatario_email]

    # Datos que se inyectarán en la plantilla HTML
    contexto = {
        'nombre': nombre_usuario,
        'mensaje': mensaje_personalizado,
        'url_accion': url,
        'texto_boton': 'Ir a la plataforma'
    }

    # Renderizar el archivo HTML con los datos
    html_contenido = render_to_string('emails/notificacion.html', contexto)
    
    # Crear una versión alternativa en texto plano para evitar filtros de spam
    texto_plano = strip_tags(html_contenido)

    # Construir y enviar el correo multiparte
    email = EmailMultiAlternatives(asunto, texto_plano, remitente, destinatarios)
    email.attach_alternative(html_contenido, "text/html")
    email.send()