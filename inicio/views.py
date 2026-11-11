from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from usuarios.models import Establecimiento, Usuario
from .forms import SolicitudMiembroForm
from admin_panel.models import Servicio 
from django.db.models import Count, Q

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

#PAGINA PRINCIPAL HOSPEDAJE: consultar a la base de datos y filtrar únicamente los establecimientos cuyo tipo sea 'Hotel'

def pagina_hospedaje(request):
    """
    Gestiona el filtrado dinámico de establecimientos según los tipos y servicios 
    seleccionados por el usuario a través del formulario lateral.
    """
    
    # 1. Por defecto, si no se selecciona nada, puedes mostrar hoteles o todos los alojamientos.
    # Aquí capturamos los valores enviados por el formulario (método GET)
    tipos_seleccionados = request.GET.getlist('tipo')
    servicios_seleccionados = request.GET.getlist('servicios')

    # 2. Partimos de la consulta base de establecimientos de hospedaje
    establecimientos = Establecimiento.objects.all().prefetch_related('servicios')

    # 3. Si el usuario marcó tipos de propiedad, filtramos por ellos
    if tipos_seleccionados:
        establecimientos = establecimientos.filter(tipo__in=tipos_seleccionados)
    else:
        # Por defecto, si entra por primera vez, mostramos 'Hotel' (o déjalo libre si prefieres)
        establecimientos = establecimientos.filter(tipo__iexact='Hotel')

    # 4. Si el usuario marcó servicios, filtramos los establecimientos que contengan ESOS servicios
    if servicios_seleccionados:
        for servicio_id in servicios_seleccionados:
            establecimientos = establecimientos.filter(servicios__id=servicio_id)

    # Evitamos duplicados si un establecimiento cumple con múltiples servicios
    establecimientos = establecimientos.distinct()

    # 5. Conteo global para los números del panel lateral (independiente de los filtros aplicados)
    total_hoteles = Establecimiento.objects.filter(tipo__iexact='Hotel').count()
    total_cabanas = Establecimiento.objects.filter(tipo__iexact='Cabaña').count()
    total_glamping = Establecimiento.objects.filter(tipo__iexact='Glamping').count()
    total_hostales = Establecimiento.objects.filter(tipo__iexact='Hostal').count()

    # 6. Servicios con conteo dinámico
    servicios_disponibles = Servicio.objects.annotate(
        total_hoteles=Count('servicios_establecimiento', filter=Q(servicios_establecimiento__tipo__iexact='Hotel'))
    )

    context = {
        'hoteles': establecimientos, # Pasamos la lista ya filtrada
        'servicios_disponibles': servicios_disponibles,
        'total_hoteles': total_hoteles,
        'total_cabanas': total_cabanas,
        'total_glamping': total_glamping,
        'total_hostales': total_hostales,
        'tipos_seleccionados': tipos_seleccionados,
        'servicios_seleccionados': servicios_seleccionados,
    }
    
    return render(request, 'index/hospedaje.html', context)