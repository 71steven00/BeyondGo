from django.shortcuts import render

# Create your views here.
def visualizar_template(request):
    return render(request, 'admin_general/gestion_usuarios.html')


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

    