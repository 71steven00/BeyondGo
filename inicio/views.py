from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from usuarios.models import Establecimiento, Usuario
from .forms import SolicitudMiembroForm

# Create your views here.
def pagina_inicio(request):
    return render(request, 'index/inicio.html')


def hazte_miembro(request):
    form = SolicitudMiembroForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        datos = form.cleaned_data
        rol = 'ADMIN_H' if datos['tipo_establecimiento'] == 'Hotel' else 'ADMIN_R'

        try:
            with transaction.atomic():
                usuario = Usuario.objects.create_user(
                    email=datos['email_contacto'],
                    password=None,
                    first_name=datos['nombre_propietario'].strip(),
                    telefono=datos['telefono'],
                    rol=rol,
                    is_active=False,
                )
                Establecimiento.objects.create(
                    usuario=usuario,
                    nombre=datos['nombre_establecimiento'].strip(),
                    tipo=datos['tipo_establecimiento'],
                    direccion=datos['direccion'].strip(),
                    ciudad=datos['ciudad'].strip(),
                    descripcion=datos['descripcion'].strip(),
                    rtn=datos.get('rnt_file'),
                    licencia_sanitaria=datos.get('sanidad_file'),
                    camara_comercio=datos.get('camara_comercio_file'),
                    is_active=False,
                    estado_revision='pendiente',
                )
        except IntegrityError:
            form.add_error('email_contacto', 'Ya existe una cuenta registrada con este correo.')
        else:
            messages.success(request, 'Tu solicitud fue enviada. Te notificaremos por correo cuando sea revisada.')
            return redirect('hazte_miembro')

    return render(request, 'index/Formulario_hazte_miembro.html', {'form': form})
