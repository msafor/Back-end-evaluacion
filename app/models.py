from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

TIPO_USUARIO_CHOICES=(
    ('ADMIN','Administrador'),
    ('VET','Veterinario'),
    ('REC','Recepcionista'),
    ('CLI','Cliente')
)

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rut_dni = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)
    tipo_usuario = models.CharField(max_length=5,choices=TIPO_USUARIO_CHOICES)
    def __str__(self):
        return f"{self.usuario.username}- {self.tipo_usuario}"


class Cliente(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    fecha_de_registro = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Dueño: {self.usuario.first_name} {self.usuario.last_name}"
    class Meta:
        ordering = ["usuario__last_name"]

class Veterinario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=70)
    licencia_profesional = models.CharField(max_length=100)
    def __str__(self):
        return f"Veterinario: {self.usuario.first_name} {self.usuario.last_name} ({self.especialidad})"

ESTADO_CHOICES=(
    ('ACTIVO',"Activo"),
    ('INACTIVO',"Inactivo")
)

SEXO_CHOICES=(
    ('M','Macho'),
    ('H','Hembra')
)

class Mascota(models.Model):
    dueño = models.ForeignKey(Cliente,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=70)
    especie = models.CharField(max_length=70)
    raza = models.CharField(max_length=70)
    fecha_nacimiento= models.DateField()
    sexo = models.CharField(max_length=1,choices=SEXO_CHOICES)
    color = models.CharField(max_length=70)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    def __str__(self):
        return f"{self.nombre} ({self.especie} - {self.raza})"
    def clean(self):
        if self.fecha_nacimiento and self.fecha_nacimiento >=date.today():
            raise ValidationError("La fechas de nacimiento no puede ser posterios o igual a hoy")
ESTADO_CITA_CHOICES=(
    ("PROG","Programada"),
    ("COMP","Completada"),
    ("CANC","Cancelada")
)

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
class Cita(models.Model):
    mascota = models.ForeignKey(Mascota,on_delete=models.CASCADE)
    veterinario = models.ForeignKey(Veterinario,on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    motivo_consulta = models.CharField(max_length=200)
    estado = models.CharField(max_length=5,choices=ESTADO_CITA_CHOICES)
    observaciones = models.CharField(max_length=70, blank=True, null=True)
    
    def __str__(self):
        return f"Cita {self.estado} para {self.mascota.nombre}"
    class Meta:
        ordering = ['fecha_hora']

class Consulta(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    fecha_de_consulta = models.DateTimeField()
    diagnostico = models.CharField(max_length=200)
    tratamiento_prescrito = models.CharField(max_length=200)
    medicamentos = models.ManyToManyField(Medicamento,blank=True)
    proxima_cita = models.DateTimeField(null=True,blank=True)
    costo_de_consulta = models.IntegerField()
    
    def __str__(self):
        return f"Diagnostico de {self.cita.mascota.nombre} ({self.fecha_de_consulta})"
    def clean(self):
        if self.costo_de_consulta < 5000 or self.costo_de_consulta >200000:
            raise ValidationError("El costo de la consulta debe estar entre $5000 y $200000")