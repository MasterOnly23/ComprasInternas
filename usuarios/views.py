from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import EditArea, CambiarContraseña,EditarDatosUsuario, EditLegajo
from usuarios.models import Area, Legajo

from django.contrib import messages

from django.contrib.auth import login, logout, authenticate, update_session_auth_hash

from tienda.views import index
# Create your views here.

@login_required
def edit_area(request):
    user = request.user

    #comprobar permisos
    is_staff = user.groups.filter(name='Staff').exists()

    user_data = Area.objects.get(user__id = user.id)
    if request.method == 'POST':
            form = EditArea(request.POST)
            if form.is_valid():
                #Datos que se van a actualizar
                user_data.area = form.cleaned_data['area']
                user_data.save()
                messages.success(request, "Los cambios se realizaron correctamente")
                return redirect(index)
    else:
            form = EditArea()
    return render(request, 'editArea.html', {'form': form, 'user': user, 'is_staff':is_staff})


@login_required
def edit_legajo(request):
    user = request.user

    #comprobar permisos
    is_staff = user.groups.filter(name='Staff').exists()

    user_data = Legajo.objects.get(user__id = user.id)
    if request.method == 'POST':
            form = EditLegajo(request.POST)
            if form.is_valid():
                #Datos que se van a actualizar
                user_data.legajo = form.cleaned_data['legajo']
                user_data.save()
                messages.success(request, "Los cambios se realizaron correctamente")
                return render(request, 'perfil.html')
    else:
            form = EditLegajo()
    return render(request, 'editLegajo.html', {'form': form, 'user': user, 'is_staff':is_staff})


@login_required
def edit_pass(request):
    user = request.user

    #comprobar permisos
    is_staff = user.groups.filter(name='Staff').exists()

    if request.method == 'POST':
        form = CambiarContraseña(data = request.POST, user = request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "La contraseña se cambio correctamente")
            return render(request, 'perfil.html')

    else:
        form = CambiarContraseña(user = request.user)
    return render(request, 'editPass.html', {'form': form, 'user': user, 'is_staff':is_staff})


@login_required
def edit_user(request):
    user = request.user

    #comprobar permisos
    is_staff = user.groups.filter(name='Staff').exists()

    user_data = User.objects.get(id = user.id)
    if request.method == 'POST':
        form = EditarDatosUsuario(request.POST)
        if form.is_valid():
            #Datos que se van a actualizar
            user_data.first_name = form.cleaned_data.get('first_name')
            user_data.last_name = form.cleaned_data.get('last_name')
            user_data.save()
            messages.success(request, "Los datos se modificaron correctamente")
            return render(request, 'perfil.html')

    else:
        form = EditarDatosUsuario(initial={'first_name': user.first_name, 'last_name': user.last_name, 'is_staff':is_staff})
    return render(request, 'editDataUser.html', {'form': form, 'user': user, 'is_staff':is_staff})
    
