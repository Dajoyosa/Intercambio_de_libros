
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


class Intercambio(models.Model):

    TIPO_ESTADO = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
        ('completado', 'Completado'),
    ]

    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='intercambios',
        verbose_name=_("Libro")
    )
    solicitante = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='solicitudes',
        verbose_name=_("Solicitante")
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de solicitud"))
    fecha_intercambio = models.DateTimeField(blank=True, null=True, verbose_name=_("Fecha de intercambio"))
    estado = models.CharField(
        max_length=20,
        choices=TIPO_ESTADO,
        default='pendiente',
        verbose_name=_("Estado")
    )
    mensaje = models.TextField(blank=True, verbose_name=_("Mensaje"))

    nombres_completos = models.CharField(max_length=200, blank=True, null=True)
    dni_contacto = models.CharField(max_length=20, blank=True, null=True)
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True)
    direccion_contacto = models.CharField(max_length=255, blank=True, null=True)
    codigo_postal_contacto = models.CharField(max_length=20, blank=True, null=True)
    pais_contacto = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = _("Intercambio")
        verbose_name_plural = _("Intercambios")
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Intercambio de {self.libro} - {self.solicitante}"



class Comentario(models.Model):

    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name=_("Libro")
    )
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name=_("Autor"))
    contenido = models.TextField(verbose_name=_("Contenido"))
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de creación"))

    class Meta:
        verbose_name = _("Comentario")
        verbose_name_plural = _("Comentarios")
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Comentario de {self.autor} en {self.libro}"


class Envio(models.Model):

    intercambio = models.OneToOneField('Intercambio', on_delete=models.CASCADE)

    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)
    pais_destino = models.CharField(max_length=100, blank=True, null=True)

    empresa_envio = models.CharField(max_length=100, blank=True, null=True)  # ej: DHL, UPS, etc.
    numero_guia = models.CharField(max_length=100, blank=True, null=True)    # número de tracking
    fecha_envio = models.DateField(blank=True, null=True)                    # fecha real del envío

    recibido = models.BooleanField(default=False)                            # si ya se recibió
    fecha_recepcion = models.DateField(blank=True, null=True)               # cuándo se recibió realmente

    celular_contacto = models.CharField(max_length=20, blank=True, null=True)
    direccion_envio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Envío del intercambio {self.intercambio.id}'


