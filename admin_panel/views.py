from django.views.decorators.cache import never_cache
from usuarios.views import limpiar_mensajes_previos
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from usuarios.decorators import rol_requerido
from usuarios.models import Usuario, Guia
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from usuarios.forms import UsuarioForm
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
            form_editar_usuario = UsuarioForm
            if request.method == 'POST':
                form = form_editar_usuario(request.POST, request.FILES, instance=user)
                if form.is_valid():
                    form.save()
                    limpiar_mensajes_previos(request)
                    messages.success(request, 'Usuario actualizado con éxito.')
                    return redirect('gestion_usuarios')
            else:
                form = form_editar_usuario(instance=user)

        elif a == 'estado' and user:
            if request.method == 'POST':
                if user == request.user:
                    limpiar_mensajes_previos(request)
                    messages.error(request, 'No puedes desactivar tu propia cuenta mientras estás en sesión activa.')
                    return redirect('gestion_usuarios')

                user.is_active = not user.is_active
                user.save()
                limpiar_mensajes_previos(request)
                estado_str = "activado" if user.is_active else "desactivado"
                messages.info(request, f'El usuario {user.get_full_name() or user.email} ha sido {estado_str}.')
                return redirect('gestion_usuarios')

        elif a == 'eliminar' and user:
            if request.method == 'POST':
                if user == request.user:
                    limpiar_mensajes_previos(request)
                    messages.error(request, 'No puedes eliminar tu propia cuenta mientras estás en sesión activa.')
                    return redirect('gestion_usuarios')

                # Verificación de dependencias (Establecimientos vinculados)
                if hasattr(user, 'establecimientos') and user.establecimientos.exists():
                    nombres_est = list(user.establecimientos.values_list('nombre', flat=True)[:3])
                    lista_est = ", ".join(f'"{nom}"' for nom in nombres_est)
                    total_est = user.establecimientos.count()
                    if total_est > 3:
                        lista_est += f" y {total_est - 3} más"

                    limpiar_mensajes_previos(request)
                    messages.error(
                        request,
                        f'No se puede eliminar a {user.first_name or user.email}: administra {total_est} establecimiento(s) ({lista_est}). Debes reasignar o eliminar los establecimientos primero, o desactivar la cuenta.'
                    )
                    return redirect('gestion_usuarios')

                nombre_usuario = user.get_full_name() or user.email
                user.delete()
                limpiar_mensajes_previos(request)
                messages.warning(request, f'Usuario {nombre_usuario} eliminado correctamente.')
                return redirect('gestion_usuarios')
            
        
        
    # =========================================================================
    # PASO D: OPTIMIZACIÓN SQL DE MÉTRICAS GLOBALES (UNA SOLA CONSULTA)
    # En lugar de ejecutar 10 consultas COUNT por separado, usamos aggregate()
    # con filtros condicionales Q() para obtener todas las estadísticas en un solo viaje a la BD.
    # =========================================================================
    ahora = timezone.now()
    inicio_mes_actual = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    primer_dia_mes_anterior = (inicio_mes_actual - timedelta(days=1)).replace(day=1)

    metricas = Usuario.objects.aggregate(
        total=models.Count('id'),
        activos=models.Count('id', filter=models.Q(is_active=True)),
        pendientes=models.Count('id', filter=models.Q(is_active=False)),
        turistas=models.Count('id', filter=models.Q(rol="TURISTA")),
        guias=models.Count('id', filter=models.Q(rol="GUIA")),
        restaurantes=models.Count('id', filter=models.Q(rol="ADMIN_R")),
        hoteles=models.Count('id', filter=models.Q(rol="ADMIN_H")),
        admins=models.Count('id', filter=models.Q(rol="ADMIN")),
        activos_este_mes=models.Count('id', filter=models.Q(is_active=True, date_joined__gte=inicio_mes_actual)),
        activos_mes_anterior=models.Count('id', filter=models.Q(is_active=True, date_joined__gte=primer_dia_mes_anterior, date_joined__lt=inicio_mes_actual))
    )

    total_usuarios = metricas['total']
    usuarios_activos = metricas['activos']
    pendientes_verificacion = metricas['pendientes']
    cant_turistas = metricas['turistas']
    cant_guias = metricas['guias']
    cant_restaurantes = metricas['restaurantes']
    cant_hoteles = metricas['hoteles']
    cant_admins = metricas['admins']
    activos_este_mes = metricas['activos_este_mes']
    activos_mes_anterior = metricas['activos_mes_anterior']

    # Cálculo del porcentaje de crecimiento comparativo mensual
    if activos_mes_anterior > 0:
        porcentaje_crecimiento = round(((activos_este_mes - activos_mes_anterior) / activos_mes_anterior) * 100)
    else:
        porcentaje_crecimiento = 100 if activos_este_mes > 0 else 0

    # =========================================================================
    # PASO D: LISTADO, BÚSQUEDA Y FILTRADO AVANZADO DE USUARIOS
    # Obtenemos los parámetros GET enviados desde el formulario de búsqueda/filtros
    # =========================================================================
    busqueda_q = request.GET.get('q', '').strip()
    filtro_rol = request.GET.get('rol', '').strip()
    filtro_estado = request.GET.get('estado', '').strip()

    # QuerySet base ordenado por fecha de registro descendente
    usuarios = Usuario.objects.all().order_by('-date_joined')

    # 1. Filtro por término de búsqueda (nombre, apellido, email, número de documento)
    if busqueda_q:
        usuarios = usuarios.filter(
            models.Q(first_name__icontains=busqueda_q) |
            models.Q(last_name__icontains=busqueda_q) |
            models.Q(email__icontains=busqueda_q) |
            models.Q(numero_documento__icontains=busqueda_q)
        )

    # 2. Filtro por rol específico
    if filtro_rol:
        usuarios = usuarios.filter(rol=filtro_rol)

    # 3. Filtro por estado activo / inactivo
    if filtro_estado == 'activo':
        usuarios = usuarios.filter(is_active=True)
    elif filtro_estado == 'inactivo':
        usuarios = usuarios.filter(is_active=False)

    # --- PAGINACIÓN ---
    # Mostramos 8 usuarios por página sobre el QuerySet filtrado
    paginator = Paginator(usuarios, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user': user,
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
        # Parámetros para mantener el estado de búsqueda y filtros en la vista y paginación
        'busqueda_q': busqueda_q,
        'filtro_rol': filtro_rol,
        'filtro_estado': filtro_estado,
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
                # IMPORTANTE: Se añade request.FILES para procesar los archivos nuevos o actualizados
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
