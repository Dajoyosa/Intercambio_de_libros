from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from libros import views
from libros.models import Libro 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('libros/', include('libros.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
