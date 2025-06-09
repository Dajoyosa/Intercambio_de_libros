from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.listar_libros, name='listar_libros'),
    path('detalle/<int:pk>/', views.detalle_libro, name='detalle_libro'),
    path('agregar/', views.agregar_libro, name='agregar_libro'),
    path('editar/<int:pk>/', views.editar_libro, name='editar_libro'),
    path('eliminar/<int:pk>/', views.eliminar_libro, name='eliminar_libro'),
    path('mis-libros/', views.mis_libros, name='mis_libros'),
    path('solicitar-intercambio/<int:libro_id>/', views.solicitar_intercambio, name='solicitar_intercambio'),
    path('gestionar-intercambio/<int:intercambio_id>/<str:accion>/', views.gestionar_intercambio, name='gestionar_intercambio'),
    path('mis-intercambios/', views.mis_intercambios, name='mis_intercambios'),
    path('agregar-comentario/<int:libro_id>/', views.agregar_comentario, name='agregar_comentario'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('envio/<int:intercambio_id>/', views.gestionar_envio, name='gestionar_envio'),
]
