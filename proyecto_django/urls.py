from django.contrib import admin
from django.urls import path
from app import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', v.iniciar_sesion),
    path('register/', v.registrarse, name="registrar"),
    path('', v.login_usuario, name='login'),
    path('registro/', v.registrar_usuario, name='registro'),
    path('inicio/', v.inicio, name='inicio'),
    path('logout/', v.logout_usuario, name='logout'),
    path('clientes/', v.listar_clientes, name='listar_clientes'),
    path('clientes/eliminar/<int:id>/', v.eliminar_cliente, name='eliminar_cliente'),
    path('veterinarios/', v.listar_veterinarios, name='listar_veterinarios'),
    path('veterinarios/crear/', v.crear_veterinario, name='crear_veterinario'),
    path('veterinarios/editar/<int:id>/', v.editar_veterinario, name='editar_veterinario'),
    path('veterinarios/eliminar/<int:id>/', v.eliminar_veterinario, name='eliminar_veterinario'),
    path('recepcionistas/', v.listar_recepcionistas, name='listar_recepcionistas'),
    path('recepcionistas/crear/', v.crear_recepcionista, name='crear_recepcionista'),
    path('recepcionistas/eliminar/<int:id>/', v.eliminar_recepcionista, name='eliminar_recepcionista'),
    path('mascotas/', v.listar_mascotas, name='listar_mascotas'),
    path('mascotas/crear/', v.crear_mascota, name='crear_mascota'),
    path('mascotas/editar/<int:id>/', v.editar_mascota, name='editar_mascota'),
    path('mascotas/eliminar/<int:id>/', v.eliminar_mascota, name='eliminar_mascota'),
    path('citas/', v.listar_citas, name='listar_citas'),
    path('citas/crear/', v.crear_cita, name='crear_cita'),
    path('citas/agendar/<int:consulta_id>/', v.agendar_proxima_cita, name='agendar_proxima_cita'),
    path('citas/editar/<int:id>/', v.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:id>/', v.eliminar_cita, name='eliminar_cita'),
    path('consultas/', v.listar_consultas, name='listar_consultas'),
    path('consultas/crear/', v.crear_consulta, name='crear_consulta'),
    path('consultas/editar/<int:id>/', v.editar_consulta, name='editar_consulta'),
    path('consultas/eliminar/<int:id>/', v.eliminar_consulta, name='eliminar_consulta'),
    path('consultas/historial/<int:mascota_id>/', v.historial_medico, name='historial_medico'),
    path('medicamentos/', v.listar_medicamentos, name='listar_medicamentos'),
    path('medicamentos/crear/', v.crear_medicamento, name='crear_medicamento'),
    path('medicamentos/editar/<int:id>/', v.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/eliminar/<int:id>/', v.eliminar_medicamento, name='eliminar_medicamento'),


]
