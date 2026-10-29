"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from usuarios.views import CustomLoginView
from django.urls import path, include
from django.conf import settings #Estas dos líneas de código en Django sirven para configurar y servir archivos multimedia
from django.conf.urls.static import static #Importa la función especial que habilita el servidor de desarrollo para entregar archivos multimedia.

urlpatterns = [
    path('', include('inicio.urls')), #ruta para administradores.urls
    path('admin/login/', CustomLoginView.as_view()),
    path('admin/', admin.site.urls),
    #Rutas principales gestionadas por usuarios y admin panel
    path('', include('usuarios.urls')),  # rutas que incluye login, registro y perfil 
    path('administrador/', include('admin_panel.urls')), #ruta para administradores.urls
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Cada vez que alguien pida una URL que empiece con /media/, busca el archivo real en la carpeta física MEDIA_ROOT y muéstralo en el navegador".

