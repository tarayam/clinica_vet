from django import forms
from django.core.exceptions import ValidationError
import re

from .models import Mascota, Dueno
from django.forms import inlineformset_factory
from .models import Atencion, Receta, RecetaItem, HoraAtencion, Veterinario


# ----- utilidades RUT -----
def _rut_normalize(value: str):
    """Quita puntos/guiones y separa cuerpo + DV (devuelve (cuerpo, DV) en mayúscula)."""
    if not value:
        return None, None
    v = re.sub(r'[^0-9kK]', '', value)  # deja solo dígitos y k/K
    if len(v) < 2:
        return None, None
    return v[:-1], v[-1].upper()

def _rut_dv(cuerpo: str) -> str:
    """Calcula DV con módulo 11."""
    s, m = 0, 2
    for d in reversed(cuerpo):
        s += int(d) * m
        m = 2 if m == 7 else m + 1
    r = 11 - (s % 11)
    return '0' if r == 11 else 'K' if r == 10 else str(r)


class DuenoForm(forms.ModelForm):
    class Meta:
        model = Dueno
        fields = ['rut','nombres','apellidos','fono1','email','fono2']
        widgets = {
            'nombres':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'apellidos':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'fono1':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678', 'type': 'tel'}),
            'email':    forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@dominio.cl'}),
            'fono2':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional', 'type': 'tel'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # UX: placeholder, pattern y autofocus
        self.fields['rut'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678-5',
            'pattern': r'[0-9\.\-kK]{7,12}',
            'title': 'Formato: 12345678-5 o 12.345.678-5',
            'autofocus': 'autofocus',
        })

    def clean_rut(self):
        rut = self.cleaned_data.get('rut', '') or ''
        cuerpo, dv = _rut_normalize(rut)
        if not cuerpo or not cuerpo.isdigit():
            raise ValidationError('RUT inválido. Ingrese números y dígito verificador (ej: 12.345.678-5).')
        esperado = _rut_dv(cuerpo)
        if dv != esperado:
            raise ValidationError('RUT inválido: dígito verificador no coincide. Reingrese el RUT.')
        rut_normalizado = f'{cuerpo}-{dv}'
# Evita duplicado si editas o creas
        existe = Dueno.objects.filter(rut=rut_normalizado).exclude(pk=self.instance.pk).exists()
        if existe:
            raise ValidationError('Este RUT ya está registrado en el sistema.')
        return rut_normalizado
        # guardamos normalizado: 12345678-5 (sin puntos)
        return f'{cuerpo}-{dv}'


# ---- el resto de tus forms tal como están ----

class MascotaForm(forms.ModelForm):
    dueno = forms.ModelChoiceField(
        queryset=Dueno.objects.order_by('apellidos', 'nombres'),
        empty_label="— Selecciona un dueño —",
        label="Dueño/a",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Mascota
        fields = ['especie','dueno','nombre','sexo','edad','n_chip','raza','imagen']
        widgets = {
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'sexo':    forms.Select(attrs={'class': 'form-select'}),
            'edad':    forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'n_chip':  forms.TextInput(attrs={'class': 'form-control'}),
            'raza':    forms.TextInput(attrs={'class': 'form-control'}),
            'nombre':  forms.TextInput(attrs={'class': 'form-control'}),
            'imagen':  forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class AtencionForm(forms.ModelForm):
    class Meta:
        model = Atencion
        fields = ['diagnostico', 'tratamiento', 'observaciones', 'fecha_control']
        widgets = {
            'diagnostico':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Síntomas, hallazgos, etc.'}),
            'tratamiento':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Medicamentos, dosis, cuidados...'}),
            'observaciones':forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Notas complementarias'}),
            'fecha_control':forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class RecetaItemForm(forms.ModelForm):
    class Meta:
        model = RecetaItem
        fields = ['medicamento', 'indicaciones']
        widgets = {
            'medicamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre comercial / genérico'}),
            'indicaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dosis, frecuencia, duración'}),
        }

RecetaItemFormSet = inlineformset_factory(
    Receta,
    RecetaItem,
    form=RecetaItemForm,
    extra=2,            # muestra 2 filas nuevas por defecto
    can_delete=True
)

class HoraAtencionForm(forms.ModelForm):
    class Meta:
        model = HoraAtencion
        fields = ['mascota', 'veterinario', 'inicio', 'fin']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veterinario'].queryset = (
            Veterinario.objects.select_related('user').order_by('nombre_publico', 'user__username')
        )
        self.fields['veterinario'].label_from_instance = (
            lambda obj: (obj.nombre_publico or obj.user.get_full_name() or obj.user.username).strip()
        )
        self.fields['inicio'].widget = forms.DateTimeInput(attrs={'type':'datetime-local'})
        self.fields['fin'].widget = forms.DateTimeInput(attrs={'type':'datetime-local'})
