from django.contrib import admin
from django.urls import path
from app import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', v.iniciar_sesion),
    path('register/', v.registrarse, name="registrar"),
]
