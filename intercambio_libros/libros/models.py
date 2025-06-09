
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    foto_perfil = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Libro(models.Model):
    
    TIPO_ESTADO = [
        ('disponible', 'Disponible'),
        ('intercambiado', 'Intercambiado'),
        ('reservado', 'Reservado'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name=_("Título"))
    autor = models.CharField(max_length=100, verbose_name=_("Autor"))
    isbn = models.CharField(max_length=20, blank=True, verbose_name=_("ISBN"))
    genero = models.CharField(max_length=50, verbose_name=_("Género"))
    estado = models.CharField(
        max_length=20,
        choices=TIPO_ESTADO,
        default='disponible',
        verbose_name=_("Estado")
    )
    descripcion = models.TextField(blank=True, verbose_name=_("Descripción"))
    fecha_publicacion = models.DateField(blank=True, null=True, verbose_name=_("Fecha de publicación"))
    portada = models.ImageField(upload_to='portadas/', blank=True, null=True, verbose_name=_("Portada"))
    propietario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="libros",
        verbose_name=_("Propietario")
    )
    fecha_agregado = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de agregado"))
    ubicacion = models.CharField(max_length=100, verbose_name=_("Ubicación"))

    class Meta:
        verbose_name = _("Libro")
        verbose_name_plural = _("Libros")
        ordering = ['-fecha_agregado']

    def __str__(self):
        return f"{self.titulo} - {self.autor}"












class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    genero = models.CharField(max_length=100)
    estado = models.CharField(max_length=50) 
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="libros")


class Intercambio(models.Model):
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="solicitudes")
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="ofertas")
    libro_solicitado = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name="intercambios")
    estado = models.CharField(max_length=20, choices=[("Pendiente", "Pendiente"), ("Aceptado", "Aceptado"), ("Rechazado", "Rechazado")])

class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_intercambio = models.DateTimeField(auto_now_add=True)
    comentario = models.TextField(null=True, blank=True)

