from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Usuario(AbstractUser):
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    groups = models.ManyToManyField(Group, related_name="usuario_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="usuario_permissions")

    def __str__(self):
        return self.direccion

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

