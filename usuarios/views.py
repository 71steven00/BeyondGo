from django.shortcuts import render
from usuarios.decorators import rol_requerido


# Create your views here.

# @rol_requerido('ADMIN_H')
# def panel_hotel(request):
#     return render(request, 'ruta/del/archivo.html') #Aca va el html de hoteles




# 1. Interfaz para Administrador General
@rol_requerido('ADMIN')
def dashboard_admin(request):
    # Retorna la plantilla HTML del panel general
    return render(request, 'ruta/del/archivo.html')


# 2. Interfaz para Administrador de Hotel
@rol_requerido('ADMIN_H')
def panel_hotel(request):
    # Retorna el HTML específico para gestionar el hotel
    return render(request, 'ruta/del/archivo.html')


# 3. Interfaz para Administrador de Restaurante
@rol_requerido('ADMIN_R')
def panel_restaurante(request):
    # Retorna el HTML específico para gestionar el restaurante
    return render(request, 'ruta/del/archivo.html')


# 4. Interfaz para Guía Turístico
@rol_requerido('GUIA')
def panel_guia(request):
    # Retorna la interfaz donde el guía ve sus tours asignados
    return render(request, 'ruta/del/archivo.html')


# 5. Interfaz para Cliente / Turista
@rol_requerido('TURISTA')
def inicio_turista(request):
    # Retorna el catálogo o inicio de búsquedas para turistas
    return render(request, 'ruta/del/archivo.html')



#{% if messages %}                                      {Esto va en el HTML de cada rol (ADMIN, ADMIN_HOTEL, ADMIN_RESTAURANTE, GUIA, TURISTA O CLIENTE)}
#   {% for message in messages %}                       {Esto va en el HTML de cada rol (ADMIN, ADMIN_HOTEL, ADMIN_RESTAURANTE, GUIA, TURISTA O CLIENTE)}
#     <div class="alert alert-{{ message.tags }}">      {Esto va en el HTML de cada rol (ADMIN, ADMIN_HOTEL, ADMIN_RESTAURANTE, GUIA, TURISTA O CLIENTE)}    
#       {{ message }}                                   {Esto va en el HTML de cada rol (ADMIN, ADMIN_HOTEL, ADMIN_RESTAURANTE, GUIA, TURISTA O CLIENTE)}
#     </div>                                            {Esto va en el HTML de cada rol (ADMIN, ADMIN_HOTEL, ADMIN_RESTAURANTE, GUIA, TURISTA O CLIENTE)}
#   {% endfor %}                                        {Esto va en el HTML de cada rol (ADMIN, ADMIN_HOTEL, ADMIN_RESTAURANTE, GUIA, TURISTA O CLIENTE)}
# {% endif %}                                           {Esto va en el HTML de cada rol (ADMIN, ADMIN_HOTEL, ADMIN_RESTAURANTE, GUIA, TURISTA O CLIENTE)}

