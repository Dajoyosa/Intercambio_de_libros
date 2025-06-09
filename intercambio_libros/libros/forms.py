from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Libro, Intercambio, Comentario, Envio

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ciudad = forms.CharField(max_length=100, required=False)
    pais = forms.CharField(max_length=100, required=False)
    biografia = forms.CharField(widget=forms.Textarea, required=False)
    foto_perfil = forms.ImageField(required=False)

    class Meta:
        model = Usuario
        fields = (
            'username', 'email', 'password1', 'password2',
            'first_name', 'last_name', 'ciudad', 'direccion',
            'telefono', 'foto_perfil'
        )


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            'titulo', 'autor', 'isbn', 'genero', 'descripcion',
            'fecha_publicacion', 'portada', 'ubicacion'
        ]
        widgets = {
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'titulo': 'Título del libro',
            'autor': 'Autor(es)',
            'isbn': 'ISBN (opcional)',
            'genero': 'Género',
            'descripcion': 'Descripción',
            'fecha_publicacion': 'Fecha de publicación',
            'portada': 'Portada del libro (opcional)',
            'ubicacion': 'Ubicación actual del libro',
        }

 
class IntercambioForm(forms.ModelForm):
    class Meta:
        model = Intercambio
        fields = [
            'mensaje', 'nombres_completos', 'dni_contacto',
            'telefono_contacto', 'direccion_contacto',
            'codigo_postal_contacto', 'pais_contacto',
        ]
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.required = name != 'codigo_postal_contacto'
 
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario aquí...'}),
        }
        labels = {
            'contenido': 'Comentario',
        }


class EnvioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = [
            'direccion_envio',
            'pais_destino',
            'ciudad',
            'codigo_postal',
            'empresa_envio',
            'numero_guia',
            'fecha_envio',
            'recibido'
        ]
        widgets = {
            'direccion_envio': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'pais_destino': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa_envio': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_guia': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_envio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'recibido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recibido'].disabled = True