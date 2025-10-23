from datetime import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from app.models import Cita, Cliente, Consulta, Mascota, Medicamento, Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]
        widgets= {
            "username": forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.TextInput(attrs={"class":"form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "password1":forms.PasswordInput(attrs={"class":"form-control"}),
            "password2":forms.PasswordInput(attrs={"class":"form-control"})
        }
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["rut_dni","telefono","tipo_usuario"]
        widgets= {
            "rut_dni": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_usuario": forms.Select(attrs={"class": "form-control"}),
        }
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["direccion"]
        widgets = {
            "direccion":forms.TextInput(attrs={"class":"form-control"})
        }

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class":"form-control"}),
            "especie":forms.TextInput(attrs={"class":"form-control"}),
            "raza": forms.TextInput(attrs={"class":"form-control"}),
            "fecha_nacimiento": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-control"}),
            "sexo": forms.Select(attrs={"class": "form-control"}),
        }

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = "__all__"
        widgets = {
            "motivo_consulta": forms.Textarea(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control"}),
            "fecha_hora": forms.DateTimeInput(attrs={"class": "form-control","type":"datetime-local"}), 
            "mascota": forms.Select(attrs={"class": "form-control"}),
            "veterinario": forms.Select(attrs={"class": "form-control"}),
        }
    def clean(self):
        cleaned_data = self.cleaned_data
        veterinario = cleaned_data.get("veterinario")
        fecha_hora = cleaned_data.get("fecha_hora")
        if fecha_hora and fecha_hora < timezone.now():
            raise ValidationError ("No se puede agendar una cita en una fecha u hora pasada")
        if fecha_hora and veterinario:
            citas_del_dia = Cita.objects.filter(
                veterinario=veterinario,
                fecha_hora__date= fecha_hora.date()
            )
        if citas_del_dia.count()>=8:
            raise ValidationError("El veterinario ya tiene 8 citas programadas para este día")
        return cleaned_data

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = "__all__"
        widgets = {
            "diagnostico": forms.Textarea(attrs={"class": "form-control"}),
            "tratamiento_prescrito": forms.Textarea(attrs={"class": "form-control"}),
            "costo_de_consulta": forms.NumberInput(attrs={"class": "form-control", "min": 5000, "max": 200000}),
            "proxima_cita": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "medicamentos": forms.SelectMultiple(attrs={"class": "form-control"}),
            "cita": forms.Select(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        diagnostico = cleaned_data.get("diagnostico")
        if diagnostico and len(diagnostico)<15:
            raise ValidationError("El diagnostico debe ser descriptivo (mínimo 15 caracteres).")
        return cleaned_data
    
class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields= "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class":"form-control"})
        }