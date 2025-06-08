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



