from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PasoEnsamblaje
import json

# Variables de estado (usar sesiones para persistencia)
paso_actual = 1
error = False

@csrf_exempt
def recibir_boton(request):
    global paso_actual, error
    if request.method == "POST":
        data = json.loads(request.body)
        boton_presionado = data.get("boton")

        if paso_actual > 4:
            return JsonResponse({"paso_actual": 5, "error": False})

        try:
            paso = PasoEnsamblaje.objects.get(orden=paso_actual)
            if boton_presionado == paso.boton_correcto:
                paso_actual += 1
                error = False
            else:
                error = True
        except PasoEnsamblaje.DoesNotExist:
            error = True

        return JsonResponse({
            "paso_actual": paso_actual,
            "error": error
        })
    return JsonResponse({"status": "error"})

@csrf_exempt
def obtener_estado(request):
    return JsonResponse({"paso_actual": paso_actual, "error": error})

def index(request): # Vista para la página de inicio
    return render(request, "ensamblaje/index.html")
