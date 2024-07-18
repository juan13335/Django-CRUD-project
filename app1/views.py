from django.shortcuts import render, redirect, get_object_or_404
# Formulario de registro e inicio de sesion
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Permite crear el usuario y guardarlo
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.


def main(request):
    return render(request, 'main.html')


def singup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()  # Guarda la informacion dentro de la BD
                login(request, user)  # Crea la cockie en la pagina
                return redirect('home')
            except IntegrityError:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'singup.html', {
                'form': UserCreationForm,
                'error': 'Las contraseñas no coinciden'
            })

@login_required
def singout(request):
    logout(request)  # Elimina el cockie del sitio web
    return redirect('home')


def singin(request):
    if request.method == 'GET':
        return render(request, 'singin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(  # Permite verificar si el usuario y la contraseña existe
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'singin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('home')

@login_required
def create_form(request):
    if request.method == 'GET':
        return render(request, 'crear_formulario.html', {
            'form': Crearformulario
        })
    else:
        try:
            # Iniicializa el formulario con los datos del usuario
            form = Crearformulario(request.POST)
            # Toma el formulario creado pero no lo guarda todavia en la BD, esto permite hacer cambios
            nuevo_form = form.save(commit=False)
            # vincula el usuario que hizo la peticion con el formulario creado
            nuevo_form.user = request.user
            nuevo_form.save()  # Guarda la instancia en la base de datos
            return redirect('home')
        except ValueError:
            return render(request, 'crear_formulario.html', {
                'form': Crearformulario,
                'error': 'Datos ingresados no son validos'
            })

@login_required
def consultar_form(request):
    # Permite consultar los datos guardados de cada usuario por eso el filter
    form = formulario.objects.filter(user=request.user, fecha_completado__isnull=True)
    return render(request, 'formularios.html', {'forms': form})

@login_required
def consultar_form_comp(request):
    # Permite consultar los datos guardados de cada usuario por eso el filter
    form = formulario.objects.filter(user=request.user, fecha_completado__isnull=False).order_by('-fecha_completado')
    return render(request, 'completados.html', {'forms': form})

@login_required
def detalle_form(request, det_id):
    if request.method == 'GET':
        # El get_object_or_404 permite mostrar una pagina 404 cuando no se encuentra el id y no mostrar formularios hecho por otro id
        detalle = get_object_or_404(formulario, pk=det_id, user=request.user)
        form = Crearformulario(instance=detalle)
        return render(request, 'detalle_form.html', {'detalle': detalle, 'form': form})
    else:
        try:
            detalle = get_object_or_404(
                formulario, pk=det_id, user=request.user)
            # Se utiliza el formulario creado previamente para completar con los datos y actualizarlos
            form = Crearformulario(request.POST, instance=detalle)
            form.save()
            return redirect('listarform')
        except ValueError:
            return render(request, 'detalle_form.html',
                          {'detalle': detalle, 'form': form, 'error': 'Error al actualizar datos'})

@login_required
def form_completo(request, det_id):
    detalle = get_object_or_404(formulario, pk=det_id, user=request.user)
    if request.method == 'POST':
        # Registra como formulario/tarea completado/a agregando la fecha
        detalle.fecha_completado = timezone.now()
        detalle.save()
        return redirect('listarform')

@login_required
def form_eliminado(request, det_id):
    detalle = get_object_or_404(formulario, pk=det_id, user=request.user)
    if request.method == 'POST':
        detalle.delete()

        return redirect('listarform')