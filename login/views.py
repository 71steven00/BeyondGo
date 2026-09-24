from django.shortcuts import render
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from usuarios.models import Usuario


@method_decorator(login_required, name='dispatch')
class PerfilUsuarioView(DetailView):
    model = Usuario
    template_name = 'login/perfil.html'
    context_object_name = 'usuario'

    def get_object(self):
        return self.request.user

def registro(request):
    return render(request, 'registro.html')
