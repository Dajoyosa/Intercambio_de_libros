<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroUsuarioForm

# Create your views here.
def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')  # o la ruta que tengas definida
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})


=======
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Libro, Intercambio, Usuario
from .forms import IntercambioForm

>>>>>>> 030bc20e98e2dd6ffcf1dee5a782996df4ea2c2d

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'libros/lista_libros.html', {'libros': libros})


def solicitar_intercambio(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        form = IntercambioForm(request.POST)
        if form.is_valid():
            intercambio = form.save(commit=False)
            intercambio.solicitante = request.user
            intercambio.propietario = libro.propietario
            intercambio.libro_solicitado = libro
            intercambio.estado = "Pendiente"
            intercambio.save()
            return redirect('detalle_libro', libro_id=libro.id)
    else:
        form = IntercambioForm()

    return render(request, 'libros/solicitar_intercambio.html', {'form': form, 'libro': libro})

def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    intercambios = Intercambio.objects.filter(libro_solicitado=libro)
    
    contexto = {
        'libro': libro,
        'intercambios': intercambios,
    }
    return render(request, 'libros/detalle_libro.html', contexto)


def gestionar_intercambio(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)

    if request.user != intercambio.propietario:
        return HttpResponseForbidden("No tienes permiso para gestionar este intercambio.")

    if request.method == 'POST':
        decision = request.POST.get("decision")
        if decision == "Aceptar":
            intercambio.estado = "Aceptado"
        elif decision == "Rechazar":
            intercambio.estado = "Rechazado"
        intercambio.save()
        return redirect('detalle_libro', libro_id=intercambio.libro_solicitado.id)

    return render(request, 'libros/gestionar_intercambio.html', {'intercambio': intercambio})

def historial_intercambios(request):
    intercambios = Intercambio.objects.filter(solicitante=request.user, estado="Aceptado")
    return render(request, 'libros/historial_intercambios.html', {'intercambios': intercambios})
