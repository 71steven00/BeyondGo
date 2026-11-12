from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from usuarios.models import Establecimiento, Usuario
from .forms import SolicitudMiembroForm
import re
from admin_panel.models import Experiencia
from django.db.models import F
from django.shortcuts import get_object_or_404


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
def pagina_experiencias(request):
    experiencias = list(
        Experiencia.objects.filter(estado='Activo').order_by('-creado_en')
    )
    categoria = request.GET.get('tipo', '')
    rango_precio = request.GET.get('precio', '')

    if categoria:
        experiencias = [
            experiencia for experiencia in experiencias
            if experiencia.tipo == categoria
        ]

    rangos_precio = {
        'hasta-50000': (0, 50000),
        '50000-80000': (50000, 80000),
        'mas-80000': (80000, None),
    }
    if rango_precio in rangos_precio:
        minimo, maximo = rangos_precio[rango_precio]
        experiencias_filtradas = []
        for experiencia in experiencias:
            digitos_precio = re.sub(r'\D', '', experiencia.precio)
            if not digitos_precio:
                continue
            precio_numerico = int(digitos_precio)
            if precio_numerico >= minimo and (
                maximo is None or precio_numerico <= maximo
            ):
                experiencias_filtradas.append(experiencia)
        experiencias = experiencias_filtradas

    return render(request, 'index/experiencias.html', {
        'experiencias': experiencias,
        'tipo_seleccionado': categoria,
        'precio_seleccionado': rango_precio,
        'tipos_experiencia': Experiencia.TIPO_CHOICES,
        'fecha_seleccionada': request.GET.get('fecha', ''),
        'hay_mas_experiencias': len(experiencias) > 4,
    })


def detalle_experiencia(request, pk):
    experiencia = get_object_or_404(
        Experiencia.objects.prefetch_related('servicios'),
        pk=pk,
        estado='Activo',
    )
    Experiencia.objects.filter(pk=experiencia.pk).update(visitas=F('visitas') + 1)
    experiencia.refresh_from_db(fields=['visitas'])
    return render(request, 'index/experiencia_detalle.html', {
        'experiencia': experiencia,
    })
