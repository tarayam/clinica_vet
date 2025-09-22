from django import forms
from .models import Mascota, Dueno

class DuenoForm(forms.ModelForm):
    class Meta:
        model = Dueno
        fields = ['rut','nombres','apellidos','fono1','email','fono2']

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['especie','dueno','nombre','sexo','edad','n_chip','raza','imagen']
