from django.contrib import admin
<<<<<<< HEAD
from .models import Usuario

# Register your models here.

admin.site.register(Usuario)


=======
from .models import Usuario, Libro, Intercambio, Historial
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Libro)
admin.site.register(Intercambio)
admin.site.register(Historial)
>>>>>>> 030bc20e98e2dd6ffcf1dee5a782996df4ea2c2d
