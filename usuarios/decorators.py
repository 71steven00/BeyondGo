from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def rol_requerido(*roles_permitidos):

    """
    def rol_requerido(*roles_permitidos):: Define la función principal del decorador.

    *roles_permitidos: El asterisco * permite recibir un número indeterminado de argumentos. Así puedes pasarle un solo rol @rol_requerido('ADMIN') o múltiples roles @rol_requerido('ADMIN_H', 'ADMIN_R').
    """

    def decorator(view_func): # def decorator(view_func):: Es la función interna que recibe como parámetro view_func, la cual representa la función de tu vista en views.py que estás intentando proteger.

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # 1. Verifica si el usuario inició sesión
            if not request.user.is_authenticated:
                messages.error(request, "Debes iniciar sesión para acceder a esta página.")
                return redirect('login') # Cambia 'login' por el nombre de tu vista de login
            
            # 2. Permite el acceso si es superusuario o si su rol está en la lista permitida
            if request.user.is_superuser or request.user.rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            
            # 3. Si no cumple los requisitos, rechaza el acceso y redirige
            messages.error(request, "No tienes permisos para acceder a esta página.")
            # Intenta regresar a la página previa; si no existe, redirige al inicio
            return redirect(request.META.get('HTTP_REFERER', 'index_usuario'))
            
        return wrapper
    return decorator

