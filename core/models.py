from django.db import models
from django.contrib.auth.models import User
from datetime import time
from django.core.exceptions import ValidationError


class Especie(models.Model):  # Admin-only (equivale a Categoría)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='especies/', null=True, blank=True)
    def __str__(self): return self.nombre

class Dueno(models.Model):
    rut = models.CharField(max_length=12, unique=True)  # valida en formulario
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    fono1 = models.CharField(max_length=20)
    email = models.EmailField()
    fono2 = models.CharField(max_length=20, blank=True)
    def __str__(self): return f"{self.nombres} {self.apellidos} ({self.rut})"

SEXO = (('M','Macho'),('H','Hembra'),('I','Indeterminado'))
class Mascota(models.Model):  # CRUD en frontend (equivale a Producto)
    especie = models.ForeignKey(Especie, on_delete=models.PROTECT, related_name='mascotas')
    dueno = models.ForeignKey(Dueno, on_delete=models.PROTECT, related_name='mascotas')
    nombre = models.CharField(max_length=60)
    sexo = models.CharField(max_length=1, choices=SEXO)
    edad = models.PositiveIntegerField(help_text='Años (aprox.)')
    n_chip = models.CharField('N° de chip', max_length=30, blank=True)
    raza = models.CharField(max_length=60, blank=True)
    imagen = models.ImageField(upload_to='mascotas/', null=True, blank=True)
    def __str__(self): return f"{self.nombre} ({self.especie})"

class Veterinario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_publico = models.CharField(max_length=100)

    def __str__(self):
    # Siempre muestra algo legible en los selects
        return (self.nombre_publico or self.user.get_full_name() or self.user.username).strip()


class Atencion(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='atenciones')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT, related_name='atenciones')
    fecha = models.DateTimeField(auto_now_add=True)
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField(blank=True)
    fecha_control = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Atención {self.id} - {self.mascota.nombre}"

class Receta(models.Model):
    atencion = models.OneToOneField(Atencion, on_delete=models.CASCADE, related_name='receta')
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receta #{self.id} - {self.atencion.mascota.nombre}"

class RecetaItem(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='items')
    medicamento = models.CharField(max_length=120)
    indicaciones = models.TextField()

    def __str__(self):
        return self.medicamento

class HoraAtencion(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.PROTECT, related_name='citas')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.PROTECT, related_name='citas')
    inicio = models.DateTimeField()
    fin = models.DateTimeField()

    def clean(self):
        # sin turnos; lun-sab; 09:00–18:00
        if self.inicio.weekday() == 6 or self.fin.weekday() == 6:
            raise ValidationError("Solo se atiende de lunes a sábado (sin domingos).")
        if not (time(9,0) <= self.inicio.time() <= time(18,0) and time(9,0) <= self.fin.time() <= time(18,0)):
            raise ValidationError("Horario hábil: 09:00 a 18:00.")
        if self.fin <= self.inicio:
            raise ValidationError("La hora de término debe ser posterior al inicio.")

    def __str__(self):
        return f"{self.inicio:%Y-%m-%d %H:%M} - {self.mascota.nombre}"

