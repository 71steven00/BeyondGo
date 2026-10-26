from django.views.decorators.cache import never_cache
from usuarios.views import limpiar_mensajes_previos
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from usuarios.decorators import rol_requerido
from usuarios.models import Usuario, Guia
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from usuarios.forms import Editar_usuario, UsuarioForm
from usuarios.models import Establecimiento
from .forms import EstablecimientoForm
from .models import Experiencia        # <--- Importa tu modelo
from .forms import ExperienciaForm
from django.db import models # para las consultas Q del buscador

# Create your views here.
def visualizar_template2(request):
    return render(request, 'admin_general/solicitudes_miembros.html')

@never_cache # Se utiliza para que el navegador no guarde cache cuando se haga logout.
@rol_requerido('ADMIN')
def dashboard_super_admin(request):
    # Datos de prueba simulando lo que vendrá de la base de datos
    paquetes_mas_vendidos = [
        {
            'titulo': 'Explorador del lago de Tota',
            'descripcion': 'Ecoturismo de gran altitud de 4 días/3 noches.',
            'reservas': 1240,
            'progreso': '85%',
            'ingresos': '$345.600',
            'crecimiento': '+18%',
            'tipo_crecimiento': 'positivo'
        },
        {
            'titulo': 'Villa de Leyva Heritage',
            'descripcion': 'Histórico de 3 días/ 2 noches. Gastronómico',
            'reservas': 982,
            'progreso': '65%',
            'ingresos': '$215.900',
            'crecimiento': '+12%',
            'tipo_crecimiento': 'positivo'
        },
        {
            'titulo': 'Cocuy Glacier Tek',
            'descripcion': 'Expedición profesional de 6 días/5 noches',
            'reservas': 456,
            'progreso': '35%',
            'ingresos': '$182.400',
            'crecimiento': '-3%',
            'tipo_crecimiento': 'negativo'
        }
    ]

    context = {
        'paquetes': paquetes_mas_vendidos,
    }
    return render(request, 'admin_general/panel_control.html', context)

@never_cache # Se utiliza para que el navegador no guarde cache cuando se haga logout.
@rol_requerido('ADMIN')
def gestion_usuarios(request, pk=None, a= None):

    #validacion para que consulte un dato especifico
    if(pk!=None): 
        user= get_object_or_404(Usuario, id=pk)
    else:
        user= None    
    form = None
    
    #validacion para el funcionamiento de editar usuario
    if (a != None):
        if a == 'crear':
            if request.method == 'POST':
                form = UsuarioForm(request.POST, request.FILES)
                if form.is_valid():
                    nuevo_usuario = form.save()
                    
                    if nuevo_usuario.rol == 'GUIA':
                        certificado = form.cleaned_data.get('certificado_turismo')
                        if certificado:
                            Guia.objects.update_or_create(
                                usuario=nuevo_usuario,
                                defaults={'certificado_turismo': certificado}
                            )
                    limpiar_mensajes_previos(request)
                    messages.success(request, 'Usuario creado con éxito.')
                    return redirect('gestion_usuarios')
            else:
                form = UsuarioForm()
                
        elif a == 'editar' and user:
            if request.method == 'POST':
                form = Editar_usuario(request.POST, request.FILES, instance=user)
                if form.is_valid():
                    form.save()
                    limpiar_mensajes_previos(request)
                    messages.success(request, 'Usuario actualizado con éxito.')
                    return redirect('gestion_usuarios')
            else:
                form = Editar_usuario(instance=user)

        elif a == 'estado' and user:
            if request.method == 'POST':
                user.is_active = not user.is_active
                user.save()
                limpiar_mensajes_previos(request)
                messages.info(request, f'Estado de {user.first_name} actualizado.')
                return redirect('gestion_usuarios')

        elif a == 'eliminar' and user:
            if request.method == 'POST':
                user.delete()
                limpiar_mensajes_previos(request)
                messages.warning(request, 'Usuario eliminado correctamente.')
                return redirect('gestion_usuarios')
            
        
        
    #LISTAMOS LOS DATOS QUE SE ENCUENTRAN EN LA BASE DE DATOS
    usuarios = Usuario.objects.all().order_by('-date_joined')
    
    #METRICAS Y CONTADORES 
    total_usuarios = usuarios.count()
    usuarios_activos = usuarios.filter(is_active=True).count()
    
    pendientes_verificacion = usuarios.filter(is_active=False).count()
    ahora = timezone.now()
    inicio_mes_actual = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Inicio del mes anterior
    primer_dia_mes_anterior = (inicio_mes_actual - timedelta(days=1)).replace(day=1)

    # Usuarios registrados en el mes actual vs mes anterior
    activos_este_mes = usuarios.filter(is_active=True, date_joined__gte=inicio_mes_actual).count()
    activos_mes_anterior = usuarios.filter(is_active=True, date_joined__gte=primer_dia_mes_anterior, date_joined__lt=inicio_mes_actual).count()
    
    # --- PAGINACIÓN ---
    # Mostramos 5 usuarios por página
    paginator = Paginator(usuarios, 5) 
    page_number = request.GET.get('page')  # Capturamos el parámetro ?page=2 de la URL
    page_obj = paginator.get_page(page_number)

    # Cálculo del porcentaje de cambio
    if activos_mes_anterior > 0:
        porcentaje_crecimiento = round(((activos_este_mes - activos_mes_anterior) / activos_mes_anterior) * 100)
    else:
        # Si el mes anterior fue 0, el incremento es del 100% por cada registro nuevo
        porcentaje_crecimiento = 100 if activos_este_mes > 0 else 0
    
    cant_turistas = usuarios.filter(rol="TURISTA").count()
    cant_guias = usuarios.filter(rol="GUIA").count()
    cant_restaurantes = usuarios.filter(rol="ADMIN_R").count()
    cant_hoteles = usuarios.filter(rol="ADMIN_H").count()
    cant_admins = usuarios.filter(rol="ADMIN").count()
    
    context = {
        'user':user,
        'form': form,
        'accion': a,
        'mostrar_modal': bool(a in ['ver', 'crear', 'editar', 'estado', 'eliminar']),
        'usuarios': usuarios,
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'pendiente_usuarios': pendientes_verificacion,
        'cant_guias': cant_guias,
        'cant_turistas': cant_turistas,
        'cant_hoteles': cant_hoteles,
        'cant_restaurantes': cant_restaurantes,
        'cant_admins': cant_admins,
        'porcentaje_crecimiento': porcentaje_crecimiento,
        'page_obj': page_obj,
    }
    return render(request, 'admin_general/gestion_usuarios.html', context)

@rol_requerido('ADMIN') # Restringe el acceso exclusivamente a usuarios con rol de Administrador
def gestion_establecimientos(request, pk=None, a=None):
    
    # 1. VALIDACIÓN DE REGISTRO ESPECÍFICO
    # Si la URL incluye una primary key (pk) distinta de cero, buscamos el establecimiento o lanzamos un error 404
    if pk is not None and pk != 0:
        establecimiento = get_object_or_404(Establecimiento, id=pk)
    else:
        establecimiento = None
        
    form = None
    
    # 2. VALIDACIÓN PARA LAS ACCIONES DE LOS MODALES
    # Controla la lógica según la acción recibida en la URL ('crear', 'editar', 'estado', 'eliminar')
    if a is not None:
        if a == 'crear':
            if request.method == 'POST':
                # Instancia el formulario con los datos y archivos enviados por POST
                form = EstablecimientoForm(request.POST, request.FILES)
                if form.is_valid():
                    # Guarda temporalmente para asignar el usuario autenticado antes de registrar en la BD
                    nuevo_est = form.save(commit=False)
                    nuevo_est.usuario = request.user
                    nuevo_est.save()
                    form.save_m2m() # Guarda relaciones de muchos a muchos (servicios)
                    messages.success(request, 'Establecimiento creado con éxito.')
                    return redirect('gestion_establecimientos')
            else:
                form = EstablecimientoForm()

        elif a == 'editar' and establecimiento:
            if request.method == 'POST':
                # Carga el formulario con los datos enviados y la instancia existente para actualizar
                form = EstablecimientoForm(request.POST, request.FILES, instance=establecimiento)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Establecimiento actualizado con éxito.')
                    return redirect('gestion_establecimientos')
            else:
                # Precarga el formulario con los datos actuales del establecimiento seleccionado
                form = EstablecimientoForm(instance=establecimiento)

        elif a == 'estado' and establecimiento:
            if request.method == 'POST':
                # Alterna el estado booleano de disponibilidad del establecimiento (Activo / Inactivo)
                establecimiento.is_active = not establecimiento.is_active
                establecimiento.save()
                estado_texto = "Disponible" if establecimiento.is_active else "No disponible"
                messages.info(request, f'El establecimiento {establecimiento.nombre} ahora está {estado_texto}.')
                return redirect('gestion_establecimientos')

        elif a == 'eliminar' and establecimiento and request.method == 'POST':
            # Elimina permanentemente el registro de la base de datos tras la confirmación POST
            establecimiento.delete()
            messages.warning(request, 'Establecimiento eliminado correctamente.')
            return redirect('gestion_establecimientos')

    # 3. LISTADO GENERAL Y BÚSQUEDA
    # Obtiene todos los establecimientos ordenados del más reciente al más antiguo
    establecimientos_list = Establecimiento.objects.all().order_by('-id')
    
    query = request.GET.get('q')
    if query:
        # Filtra los resultados si el usuario ingresó un término de búsqueda
        establecimientos_list = establecimientos_list.filter(
            models.Q(nombre__icontains=query) | 
            models.Q(ciudad__icontains=query) |
            models.Q(direccion__icontains=query)
        )

    # 4. PAGINACIÓN DE LOS RESULTADOS
    # Configura la paginación para mostrar 6 establecimientos por cada página
    paginator = Paginator(establecimientos_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 5. DICCIONARIO DE CONTEXTO PARA LA PLANTILLA HTML
    context = {
        'establecimiento': establecimiento,  # Objeto específico para los modales (ver, editar, estado, eliminar)
        'form': form,                        # Instancia del formulario para las acciones de creación o edición
        'accion': a,                         # Acción activa actual en la URL
        'mostrar_modal': bool(a in ['ver', 'crear', 'editar', 'eliminar', 'estado']), # Bandera para renderizar el modal
        'establecimientos': page_obj,        # Objeto paginado con la lista de establecimientos
        'query': query,                      # Texto de búsqueda actual para conservarlo en la vista
    }
    
    return render(request, 'admin_general/gestion_establecimientos.html', context)

@rol_requerido('ADMIN')
def experiencias(request, pk=None, a=None):
    # Validación para consultar un dato específico si viene el pk
    if pk is not None:
        experiencia = get_object_or_404(Experiencia, id=pk)
    else:
        experiencia = None
        
    form = None
    
    # Validación para las acciones de los modales
    if a is not None:
        if a == 'crear':
            if request.method == 'POST':
                form = ExperienciaForm(request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Experiencia creada con éxito.')
                    return redirect('gestion_experiencias')
            else:
                form = ExperienciaForm()

        elif a == 'editar' and experiencia:
            if request.method == 'POST':
                form = ExperienciaForm(request.POST, request.FILES, instance=experiencia)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Experiencia actualizada con éxito.')
                    return redirect('gestion_experiencias')
            else:
                form = ExperienciaForm(instance=experiencia)

        elif a == 'estado' and experiencia:
            if request.method == 'POST':
                # Alterna el estado de la experiencia (ej. de Activo a Pausado)
                if experiencia.estado == 'Activo':
                    experiencia.estado = 'Pausado'
                else:
                    experiencia.estado = 'Activo'
                experiencia.save()
                messages.info(request, f'Estado de la experiencia actualizado a {experiencia.estado}.')
                return redirect('gestion_experiencias')

        elif a == 'eliminar' and experiencia and request.method == 'POST':
            experiencia.delete()
            messages.warning(request, 'Experiencia eliminada correctamente.')
            return redirect('gestion_experiencias')

    experiencias_list = Experiencia.objects.all().order_by('-id')
    
    # Paginación (opcional si usas page_obj como en usuarios)
    paginator = Paginator(experiencias_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    experiencias_destacadas = experiencias_list[:2]

    context = {
        'experiencia': experiencia,
        'form': form,
        'accion': a,
        'mostrar_modal': bool(a in ['ver', 'crear', 'editar', 'eliminar', 'estado']),
        'experiencias': page_obj,  # Usamos page_obj para la paginación consistente
        'experiencias_destacadas': experiencias_destacadas,
    }
    return render(request, 'admin_general/gestion_experiencias.html', context)
