from django.shortcuts import render, redirect
from app.forms import RegistroForm
from django.contrib.auth import login, authenticate

def iniciar_sesion(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        user = authenticate(request, username=uname, password=passw)
        if user:
            login(request, user)
            # Pendiente la redirección de home (inicio de sesion exitoso)
            return redirect("home")
        else:
            return render(request, "autenticacion/login.html", {"error": "Credenciales incorrectas"})

def registrarse(request):
    if request.method == "GET":
        form = RegistroForm()
    elif request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Pendiente la redirección de home (registro exitoso)
            return redirect("home")

    return render(request, "autenticacion/registro.html", {"form": form})