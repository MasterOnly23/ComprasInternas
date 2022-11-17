from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'productos.html')

@login_required
def perfil(request):
    return render(request, 'perfil.html')

