from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Especie, Mascota
from .forms import MascotaForm, DuenoForm

def home(request):
    especies = Especie.objects.all()
    return render(request, 'home.html', {'especies': especies})

def mascotas_por_especie(request, especie_id):
    especie = get_object_or_404(Especie, id=especie_id)
    q = request.GET.get('q', '')
    mascotas = especie.mascotas.select_related('dueno').all()
    if q:
        mascotas = mascotas.filter(Q(nombre__icontains=q) | Q(dueno__apellidos__icontains=q))
    return render(request, 'mascotas_listado.html', {'especie': especie, 'mascotas': mascotas, 'q': q})

def mascota_mantenedor(request, mascota_id=None):
    mascota = get_object_or_404(Mascota, id=mascota_id) if mascota_id else None
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MascotaForm(instance=mascota)
    return render(request, 'mascota_form.html', {'form': form, 'mascota': mascota})

def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    mascota.delete()
    return redirect('home')

def dueno_nuevo(request):
    if request.method == 'POST':
        form = DuenoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DuenoForm()
    return render(request, 'dueno_form.html', {'form': form})
