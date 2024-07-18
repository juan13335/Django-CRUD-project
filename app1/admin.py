from django.contrib import admin
from .models import formulario

class Formulariohora(admin.ModelAdmin):
    readonly_fields = ("fecha_creacion", ) # Para poder ver en pantalla campos automaticos

# Register your models here.
admin.site.register(formulario, Formulariohora) # Registrar modelo en menu de administrador