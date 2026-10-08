from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from usuarios.decorators import rol_requerido
from usuarios.models import Usuario
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from usuarios.forms import Editar_usuario, UsuarioForm

# Create your views here.
def visualizar_template2(request):
    return render(request, 'admin_general/solicitudes_miembros.html')


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
                    form.save()

                    messages.success(request, 'Usuario creado con éxito.')
                    return redirect('gestion_usuarios')
            else:
                form = UsuarioForm()
                
        elif a == 'editar' and user:
            if request.method == 'POST':
                form = Editar_usuario(request.POST, request.FILES, instance=user)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Usuario actualizado con éxito.')
                    return redirect('gestion_usuarios')
            else:
                form = Editar_usuario(instance=user)

        elif a == 'estado' and user:
            if request.method == 'POST':
                user.is_active = not user.is_active
                user.save()
                messages.info(request, f'Estado de {user.first_name} actualizado.')
                return redirect('gestion_usuarios')

        elif a == 'eliminar' and user:
            if request.method == 'POST':
                user.delete()
                messages.warning(request, 'Usuario eliminado correctamente.')
                return redirect('gestion_usuarios')
            
        
        
    #LISTAMOS LOS DATOS QUE SE ENCUEnTRAN EN LA BASE DE DATOS
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