from django.db import models

class PasoEnsamblaje(models.Model):
    orden = models.PositiveIntegerField(unique=True)
    nombre_pieza = models.CharField(max_length=50)
    led_asociado = models.PositiveIntegerField()  # Número de LED (1-4)
    boton_correcto = models.PositiveIntegerField()  # Número de botón (1-4)

    def __str__(self):
        return f"Paso {self.orden}: {self.nombre_pieza}"