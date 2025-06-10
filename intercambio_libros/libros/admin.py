from django.contrib import admin
from .models import Usuario, Libro, Intercambio
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Libro)
admin.site.register(Intercambio)
