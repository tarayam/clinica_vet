from django.db import models

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
