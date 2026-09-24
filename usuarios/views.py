from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
  template_name = 'inicio_sesion.html'

  def dispatch(self, request, *args, **kwargs):
      return self.render_to_response(self.get_context_data(form=self.get_form()))