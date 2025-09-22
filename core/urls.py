from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('especie/<int:especie_id>/', views.mascotas_por_especie, name='mascotas_por_especie'),
    path('mascota/nueva/', views.mascota_mantenedor, name='mascota_nueva'),
    path('mascota/<int:mascota_id>/editar/', views.mascota_mantenedor, name='mascota_editar'),
    path('mascota/<int:mascota_id>/eliminar/', views.eliminar_mascota, name='mascota_eliminar'),
    path('dueno/nuevo/', views.dueno_nuevo, name='dueno_nuevo'),
]
