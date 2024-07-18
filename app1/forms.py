from django import forms
from .models import *

class Crearformulario(forms.ModelForm):
    class Meta:
        model = formulario # Es obligatorio poner el nomber model como nombre de variable
        fields = ['titulo', 'descripcion', 'importancia'] 
        widgets = { # Forma de agregar estilos al formulario
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un titulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe un descripcion'}),
            'importancia': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }