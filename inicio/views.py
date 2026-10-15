from django.shortcuts import render

# Create your views here.
def visualizar_template_header(request):
    return render(request, 'index/inicio.html')