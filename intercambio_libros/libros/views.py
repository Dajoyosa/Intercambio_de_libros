from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Libro, Intercambio, Comentario, Usuario, Envio
from .forms import EnvioForm, RegistroForm, LibroForm, IntercambioForm, ComentarioForm


def inicio(request):
    ultimos_libros = Libro.objects.filter(estado='disponible').order_by('-fecha_agregado')[:6]
    total_libros = Libro.objects.filter(estado='disponible').count()
    total_usuarios = Usuario.objects.count()
    total_intercambios = Intercambio.objects.filter(estado='completado').count()
    
    context = {
        'ultimos_libros': ultimos_libros,
        'total_libros': total_libros,
        'total_usuarios': total_usuarios,
        'total_intercambios': total_intercambios,
    }
    return render(request, 'inicio.html', context)

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a nuestra plataforma.')
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def listar_libros(request):
    libros_disponibles = Libro.objects.filter(estado='disponible').order_by('-fecha_agregado')
    genero = request.GET.get('genero')
    if genero:
        libros_disponibles = libros_disponibles.filter(genero__icontains=genero)

    intercambios_en_proceso = Intercambio.objects.filter(
        estado='aceptado',
        envio__isnull=False
    )
    intercambios_en_proceso = [i for i in intercambios_en_proceso if not i.envio.recibido]
    libros_en_proceso_ids = [i.libro_id for i in intercambios_en_proceso]

    paginator = Paginator(libros_disponibles, 9)
    page_number = request.GET.get('page')
    libros = paginator.get_page(page_number)

    return render(request, 'libros/listar.html', {
        'libros': libros,
        'libros_en_proceso_ids': libros_en_proceso_ids,
    })

@login_required
def detalle_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    intercambio_existente = False
    if request.user.is_authenticated:
        intercambio_existente = Intercambio.objects.filter(libro=libro, solicitante=request.user).exists()

    comentarios = libro.comentarios.all().order_by('-fecha_creacion')

    if request.method == 'POST':
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            nuevo_comentario = comentario_form.save(commit=False)
            nuevo_comentario.libro = libro
            nuevo_comentario.autor = request.user
            nuevo_comentario.save()
            messages.success(request, 'Tu comentario ha sido agregado.')
            return redirect('detalle_libro', pk=libro.pk)
    else:
        comentario_form = ComentarioForm()

    return render(request, 'libros/detalle.html', {
        'libro': libro,
        'comentarios': comentarios,
        'comentario_form': comentario_form,
        'intercambio_existente': intercambio_existente,
    })

@login_required
def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.propietario = request.user
            libro.save()
            messages.success(request, '¡Libro agregado con éxito!')
            return redirect('mis_libros')
    else:
        form = LibroForm()
    return render(request, 'libros/agregar.html', {'form': form})

@login_required
def editar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if libro.propietario != request.user:
        messages.error(request, 'No tienes permiso para editar este libro.')
        return redirect('inicio')
    
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Libro actualizado con éxito!')
            return redirect('mis_libros')
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'libros/editar.html', {'form': form, 'libro': libro})

@login_required
def eliminar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if libro.propietario != request.user:
        messages.error(request, 'No tienes permiso para eliminar este libro.')
        return redirect('inicio')
    
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado correctamente.')
        return redirect('mis_libros')
    
    return render(request, 'libros/eliminar.html', {'libro': libro})

@login_required
def mis_libros(request):
    libros = Libro.objects.filter(propietario=request.user).order_by('-fecha_agregado')
    return render(request, 'libros/mis_libros.html', {'libros': libros})

@login_required
def solicitar_intercambio(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    
    if libro.propietario == request.user:
        messages.error(request, 'No puedes solicitar un intercambio de tu propio libro.')
        return redirect('detalle_libro', pk=libro_id)

    if Intercambio.objects.filter(libro=libro, solicitante=request.user).exists():
        messages.info(request, 'Ya has solicitado este libro anteriormente.')
        return redirect('detalle_libro', pk=libro_id)

    if request.method == 'POST':
        form = IntercambioForm(request.POST)
        if form.is_valid():
            intercambio = form.save(commit=False)
            intercambio.libro = libro
            intercambio.solicitante = request.user
            intercambio.save()
            messages.success(request, '¡Solicitud de intercambio enviada!')
            return redirect('detalle_libro', pk=libro_id)
    else:
        form = IntercambioForm()

    return render(request, 'intercambios/solicitar.html', {'form': form, 'libro': libro})

@login_required
def gestionar_intercambio(request, intercambio_id, accion):
    intercambio = get_object_or_404(Intercambio, pk=intercambio_id)
    
    if intercambio.libro.propietario != request.user:
        messages.error(request, 'No tienes permiso para gestionar este intercambio.')
        return redirect('inicio')
    
    if accion == 'aceptar':
        intercambio.estado = 'aceptado'
        intercambio.libro.estado = 'reservado'
        intercambio.libro.save()
        intercambio.save()
        messages.success(request, 'Has aceptado la solicitud de intercambio.')
    elif accion == 'rechazar':
        intercambio.estado = 'rechazado'
        intercambio.save()
        messages.info(request, 'Has rechazado la solicitud de intercambio.')
    elif accion == 'completar':
        intercambio.estado = 'completado'
        intercambio.libro.estado = 'intercambiado'
        intercambio.libro.propietario = intercambio.solicitante
        intercambio.fecha_intercambio = timezone.now()
        intercambio.libro.save()
        intercambio.save()
        messages.success(request, 'Intercambio completado con éxito.')
    
    return redirect('mis_intercambios')

@login_required
def mis_intercambios(request):
    intercambios_propietario = Intercambio.objects.filter(libro__propietario=request.user).order_by('-fecha_solicitud')
    intercambios_solicitante = Intercambio.objects.filter(solicitante=request.user).order_by('-fecha_solicitud')

    envios = {e.intercambio_id: e for e in Envio.objects.filter(intercambio__in=list(intercambios_propietario) + list(intercambios_solicitante))}

    return render(request, 'intercambios/mis_intercambios.html', {
        'intercambios_propietario': intercambios_propietario,
        'intercambios_solicitante': intercambios_solicitante,
        'envios': envios,
    })

@login_required
def agregar_comentario(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.libro = libro
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentario agregado con éxito.')
    
    return redirect('detalle_libro', pk=libro_id)

@login_required
def perfil_usuario(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})

@login_required
def gestionar_envio(request, intercambio_id):
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    envio, creado = Envio.objects.get_or_create(intercambio=intercambio)

    if request.method == 'POST':
        if 'marcar_recibido' in request.POST:
            if request.user == intercambio.solicitante:
                envio.recibido = True
                envio.estado_intercambio = 'Completado'
                envio.save()
                intercambio.estado = 'completado'
                intercambio.libro.disponible = False
                intercambio.libro.save()
                intercambio.save()
                messages.success(request, "Has marcado el envío como recibido.")
                return redirect('mis_intercambios')
            else:
                messages.error(request, "No tienes permiso para realizar esta acción.")
                return redirect('inicio')
        elif request.user == intercambio.libro.propietario:
            form = EnvioForm(request.POST, instance=envio)
            if form.is_valid():
                envio = form.save(commit=False)
                envio.intercambio = intercambio
                envio.estado_intercambio = 'Enviado'
                envio.save()
                messages.success(request, "El envío fue guardado correctamente.")
                return redirect('mis_intercambios')
            else:
                messages.error(request, "Hubo errores en el formulario.")
        else:
            messages.error(request, "No tienes permiso para modificar este envío.")
            return redirect('inicio')
    else:
        form = EnvioForm(instance=envio)

    return render(request, 'intercambios/detalle_envio.html', {
        'envio': envio,
        'intercambio': intercambio,
        'form': form
    })
    
