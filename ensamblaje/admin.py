from django.contrib import admin
from .models import PasoEnsamblaje

@admin.register(PasoEnsamblaje)
class PasoEnsamblajeAdmin(admin.ModelAdmin):
    list_display = ('orden', 'nombre_pieza', 'led_asociado', 'boton_correcto')
