from django.shortcuts import render
from axes.exceptions import AxesLocked
from django.contrib import messages
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
  template_name = 'login/inicio_sesion.html'

  def dispatch(self, request, *args, **kwargs):
    try:
      return super().dispatch(request, *args, **kwargs)
    except AxesLocked:
      messages.error(
          request,
          'Demasiados intentos fallidos. Tu cuenta ha sido bloqueada'
          ' temporalmente por seguridad.',
      )
      return self.render_to_response(self.get_context_data(form=self.get_form()))