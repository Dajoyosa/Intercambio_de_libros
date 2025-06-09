from django.contrib import admin
from .models import Usuario

# Register your models here.

admin.site.register(Usuario)

from .models import Usuario, Libro, Intercambio, Historial
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Libro)
admin.site.register(Intercambio)
admin.site.register(Historial)
