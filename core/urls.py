from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('especie/<int:especie_id>/', views.mascotas_por_especie, name='mascotas_por_especie'),
    path('mascota/nueva/', views.mascota_mantenedor, name='mascota_nueva'),
    path('mascota/<int:mascota_id>/editar/', views.mascota_mantenedor, name='mascota_editar'),
    path('mascota/<int:mascota_id>/eliminar/', views.eliminar_mascota, name='mascota_eliminar'),
    path('dueno/nuevo/', views.dueno_nuevo, name='dueno_nuevo'),
    # Atención (veterinario)
    path('mascota/<int:mascota_id>/atencion/nueva/', views.atencion_nueva, name='atencion_nueva'),

# Agenda (asistente)
    path('agenda/', views.agenda_list, name='agenda_list'),
    path('agenda/nueva/', views.hora_nueva, name='hora_nueva'),
    path('agenda/<int:hora_id>/editar/', views.hora_editar, name='hora_editar'),
    path('agenda/<int:hora_id>/eliminar/', views.hora_eliminar, name='hora_eliminar'),
    path('mascota/<int:mascota_id>/detalle/', views.mascota_detalle, name='mascota_detalle'),
    path('mascotas/', views.mascotas_all, name='mascotas_all'),


]
