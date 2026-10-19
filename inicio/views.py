from django.shortcuts import render

# Create your views here.
def visualizar_template_header(request):
    return render(request, 'index/inicio.html')
def inicio(request):
    return render(request, 'inicio.html')

def hospedaje(request):
    return render(request, 'inicio.html')

def restaurantes(request):
    return render(request, 'inicio.html')

def hazte_miembro(request):
    return render(request, 'inicio.html')

def login_view(request):
    return render(request, 'inicio.html') # O tu vista de login existente
