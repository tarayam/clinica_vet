from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Especie, Mascota
from .forms import MascotaForm, DuenoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Especie, Mascota, Atencion, Receta, Veterinario, HoraAtencion
from .forms import MascotaForm, DuenoForm, AtencionForm, RecetaItemFormSet, HoraAtencionForm
from django.urls import reverse

def es_veterinario(u):
    return u.is_authenticated and u.groups.filter(name='veterinario').exists()

def es_asistente(u):
    return u.is_authenticated and u.groups.filter(name='asistente').exists()


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

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    mascota.delete()
    return redirect('home')

@login_required(login_url='/accounts/login/')
def dueno_nuevo(request):
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('mascota_nueva')
    if request.method == 'POST':
        form = DuenoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next_url)
    else:
        form = DuenoForm()
    return render(request, 'dueno_form.html', {'form': form, 'next': next_url})

@user_passes_test(es_veterinario, login_url='/accounts/login/')
def atencion_nueva(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    vet = get_object_or_404(Veterinario, user=request.user)

    if request.method == 'POST':
        aform = AtencionForm(request.POST)
        if aform.is_valid():
            at = aform.save(commit=False)
            at.mascota = mascota
            at.veterinario = vet
            at.save()
            receta = Receta.objects.create(atencion=at)
            formset = RecetaItemFormSet(request.POST, instance=receta)
            if formset.is_valid():
                formset.save()
                return redirect('mascota_editar', mascota_id=mascota.id)
    else:
        aform = AtencionForm()
        # receta aún no existe; creamos formset sin instancia y al guardar lo ligamos
        receta = Receta()  # dummy para construir el formset
        formset = RecetaItemFormSet(instance=receta)

    return render(request, 'atencion_form.html', {
        'aform': aform,
        'formset': formset,
        'mascota': mascota
    })

@user_passes_test(es_asistente, login_url='/accounts/login/')
def agenda_list(request):
    ahora = timezone.now()
    citas = HoraAtencion.objects.select_related('mascota','veterinario').order_by('inicio')
    return render(request, 'agenda_list.html', {'citas': citas})

@user_passes_test(es_asistente, login_url='/accounts/login/')
def hora_nueva(request):
    if request.method == 'POST':
        form = HoraAtencionForm(request.POST)
        if form.is_valid():
            form.instance.clean()  # valida horario
            form.save()
            return redirect('agenda_list')
    else:
        form = HoraAtencionForm()
    return render(request, 'hora_form.html', {'form': form, 'titulo': 'Nueva hora'})

@user_passes_test(es_asistente, login_url='/accounts/login/')
def hora_editar(request, hora_id):
    hora = get_object_or_404(HoraAtencion, id=hora_id)
    if request.method == 'POST':
        form = HoraAtencionForm(request.POST, instance=hora)
        if form.is_valid():
            form.instance.clean()
            form.save()
            return redirect('agenda_list')
    else:
        form = HoraAtencionForm(instance=hora)
    return render(request, 'hora_form.html', {'form': form, 'titulo': 'Editar hora'})

@user_passes_test(es_asistente, login_url='/accounts/login/')
def hora_eliminar(request, hora_id):
    hora = get_object_or_404(HoraAtencion, id=hora_id)
    hora.delete()
    return redirect('agenda_list')


def mascota_detalle(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # si tienes atenciones:
    ultima_atencion = getattr(mascota, 'atenciones', None)
    ultima_atencion = ultima_atencion.order_by('-fecha').first() if ultima_atencion else None

    es_veterinario = (
        request.user.is_authenticated
        and request.user.groups.filter(name='veterinario').exists()
    )

    return render(
        request,
        'mascota_detalle.html',
        {'mascota': mascota, 'ultima_atencion': ultima_atencion, 'es_veterinario': es_veterinario}
    )
def mascotas_all(request):
    q = request.GET.get('q')
    especie_id = request.GET.get('especie')
    mascotas = Mascota.objects.select_related('especie','dueno').all()
    if especie_id:
        mascotas = mascotas.filter(especie_id=especie_id)
    if q:
        mascotas = mascotas.filter(
            Q(nombre__icontains=q) |
            Q(dueno__apellidos__icontains=q) |
            Q(dueno__nombres__icontains=q)
        )
    especies = Especie.objects.all()
    return render(request, 'mascotas_all.html', {'mascotas': mascotas, 'especies': especies, 'q': q})

