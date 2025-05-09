"""
URL configuration for produccion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ensamblaje import views
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),  # Esta línea añade una vista para la raíz "/"
    path('api/boton/', views.recibir_boton, name='recibir_boton'),
    path("api/estado/", views.obtener_estado, name="obtener_estado"),  # Nueva ruta

]

# produccion/urls.py
#def home(request):
#    return HttpResponse("¡Bienvenido a la línea de producción!")

#urlpatterns = [
#    path('', views.index, name = 'index'),  # Esta línea añade una vista para la raíz "/"
#    path('api/boton/', views.recibir_boton, name='recibir_boton'),
#]

