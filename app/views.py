from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app.forms import RegistroForm, UsuarioForm, ClienteForm, MascotaForm, CitaForm, ConsultaForm, MedicamentoForm
from app.models import Usuario, Mascota, Cliente, Cita, Veterinario, Consulta, Medicamento

def registrar_usuario(request):
    if request.method == 'POST':
        form_user = RegistroForm(request.POST)
        form_usuario = UsuarioForm(request.POST)
        form_cliente = ClienteForm(request.POST)

        if form_user.is_valid() and form_usuario.is_valid() and form_cliente.is_valid():
            form_user.save()
            form_usuario.save()
            form_cliente.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('login')
        else:
            messages.error(request, "Error en el registro, revise los datos ingresados.")
    else:
        form_user = RegistroForm()
        form_usuario = UsuarioForm()
        form_cliente = ClienteForm()

    data = {
        'form_user': form_user,
        'form_usuario': form_usuario,
        'form_cliente': form_cliente
    }
    return render(request, 'autenticacion/registro.html', data)


def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}")
            return redirect('inicio')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return redirect('login')
    return render(request, 'autenticacion/login.html')


def logout_usuario(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('login')


def inicio(request):
    usuario = Usuario.objects.get(usuario=request.user)
    tipo = usuario.tipo_usuario

    if tipo == 'ADMIN':
        return render(request, 'administrador/inicio.html', {'usuario': usuario})
    elif tipo == 'VET':
        return render(request, 'veterinario/inicio.html', {'usuario': usuario})
    elif tipo == 'REC':
        return render(request, 'recepcionista/inicio.html', {'usuario': usuario})
    elif tipo == 'CLI':
        return render(request, 'cliente/inicio.html', {'usuario': usuario})
    else:
        messages.error(request, "Tipo de usuario no reconocido.")
        return redirect('login')

def listar_veterinarios(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para ver los veterinarios")
        return redirect("inicio")
    veterinarios = Veterinario.objects.all()
    data = {"veterinarios":veterinarios}
    return render(request, "veterinarios/listar.html",data)

def crear_veterinario(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para crear veterinarios")
        return redirect("inicio")
    if request.method == "POST":
        form_user = RegistroForm(request.POST)
        form_usuario = UsuarioForm(request.POST)
        if form_user.is_valid and form_usuario.is_valid():
            user = form_user.save()
            usuario_datos = form_usuario.save()
            usuario_datos.usuario = user
            usuario_datos.tipo_usuario = "VET"
            usuario_datos.save()
            messages.success(request, "Veterinario registrado correctamente")
            return redirect("listar_veterinario")
        else:
            messages.error(request,"Error al registrar el veterinario")
    else:
        form_user = RegistroForm()
        form_usuario = UsuarioForm()
    data = {"form_user":form_user, "form_usuario":form_usuario}
    return render(request, "veterinario/crear.html", data)

def editar_veterinario(request, id):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para editar veterinarios")
        return redirect("inicio")
    veterinario = Veterinario.objects.get(id,id)
    form = UsuarioForm(request.POST or None, instance=veterinario.usuario.usuario)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,"Veterinario actualizado correctamente")
            return redirect("listar_veterinarios")
        else:
            messages.error(request,"Error al actualizar el veterinario")

    data = {"form":form, "veterinario":veterinario}
    return render(request,"veterinarios/editar.html",data)

def eliminar_veterinario(request, id):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario !="ADMIN":
        messages.error(request, "No tiene permisos para eliminar veterinarios")
        return redirect("inicio")

    veterinario = Veterinario.objects.get(id=id)
    if request.method == "POST":
        veterinario.delete()
        messages.success(request,"Veterinario eliminado correctamente")
        return redirect("listar_veterinarios")
    data= {"veterinario": veterinario}
    return render(request,"veterinario/eliminar.html",data)        

def agenda_veterinarios(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario not in ["ADMIN","REC"]:
        messages.error(request, "No tiene permisos para ver la agenda de los veterinarios")
        return redirect("inicio")
    citas = Cita.objects.all()
    data = {"citas": citas}
    return render(request, "citas/agenda_veterinarios.html",data)

def listar_recepcionistas(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para ver recepcionistas.")
        return redirect("inicio")

    recepcionistas = Usuario.objects.filter(tipo_usuario="REC")
    data = {"recepcionistas": recepcionistas}
    return render(request, "recepcionistas/listar.html", data)


def crear_recepcionista(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para crear recepcionistas.")
        return redirect("inicio")

    if request.method == "POST":
        form_user = RegistroForm(request.POST)
        form_usuario = UsuarioForm(request.POST)
        if form_user.is_valid() and form_usuario.is_valid():
            user = form_user.save()
            usuario_datos = form_usuario.save(commit=False)
            usuario_datos.usuario = user
            usuario_datos.tipo_usuario = "REC"
            usuario_datos.save()
            messages.success(request, "Recepcionista creado correctamente.")
            return redirect("listar_recepcionistas")
        else:
            messages.error(request, "Error al registrar el recepcionista.")
    else:
        form_user = RegistroForm()
        form_usuario = UsuarioForm()

    data = {"form_user": form_user, "form_usuario": form_usuario}
    return render(request, "recepcionistas/crear.html", data)


def eliminar_recepcionista(request, id):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para eliminar recepcionistas.")
        return redirect("inicio")

    recepcionista = Usuario.objects.get(id=id)
    if request.method == "POST":
        recepcionista.delete()
        messages.success(request, "Recepcionista eliminado correctamente.")
        return redirect("listar_recepcionistas")
    data = {"recepcionista": recepcionista}
    return render(request, "recepcionistas/eliminar.html", data)

def listar_clientes(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario not in ["ADMIN", "REC"]:
        messages.error(request, "No tiene permisos para ver clientes.")
        return redirect("inicio")

    clientes = Cliente.objects.all()
    data = {"clientes": clientes}
    return render(request, "clientes/listar.html", data)

def crear_cliente(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario not in ["ADMIN","REC"]:
        messages.error(request, "No tiene permisos para registrar clientes")
        return redirect("inicio")
    if request.method== "POST":
        form_user = RegistroForm(request.POST)
        form_usuario = UsuarioForm(request.POST)
        form_cliente = ClienteForm(request.POST)
        if form_user.is_valid() and form_usuario.is_valid() and form_cliente.is_valid():
            form_user.save()
            form_usuario.save()
            form_cliente.save()
            messages.success(request, "Cliente registrado correctamente")
            return redirect("listar_clientes")
        else:
            messages.error(request,"Error al registrar cliente")
    else:
        form_user= RegistroForm()
        form_usuario= UsuarioForm()
        form_cliente = ClienteForm()
    data = {"form_user": form_user, "form_usuario": form_usuario, "form_cliente":form_cliente}
    return render(request, "clientes/crear.html",data)

def eliminar_cliente(request, id):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario not in ["ADMIN", "REC"]:
        messages.error(request, "No tiene permisos para eliminar clientes.")
        return redirect("inicio")

    cliente = Cliente.objects.get(id=id)
    if request.method == "POST":
        cliente.delete()
        messages.success(request, "Cliente eliminado correctamente.")
        return redirect("listar_clientes")
    data = {"cliente": cliente}
    return render(request, "clientes/eliminar.html", data)

def listar_mascotas(request):
    usuario = Usuario.objects.get(usuario=request.user)

    if usuario.tipo_usuario not in ["ADMIN","REC","CLI"]:
        messages.error(request, "No tiene permisos para ver las mascotas")
        return redirect("inicio")
    
    if usuario.tipo_usuario == "CLI":
        cliente = Cliente.objects.get(usuario=request.user)
        mascotas = Mascota.objects.filter(dueño=cliente)
    else:
        mascotas = Mascota.objects.all()

    data = {"mascotas":mascotas}

    return render(request, "mascotas/listar.html",data)

def crear_mascota(request):
    usuario = Usuario.objects.get(usuario=request.user)

    if usuario.tipo_usuario not in ["CLI","REC"]:
        messages.error(request,"No tiene permisos para registrar mascotas.")
        return redirect("inicio")
    
    if request.method == "POST":
        form= MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save()
            messages.success(request, f"Mascota {mascota.nombre} registrada correctamente")
            return redirect("listar_mascotas")
        else:
            messages.error(request, "Error al registrar la mascota")
    else:
        form = MascotaForm()
    data = {"form":form}
    return render(request, "mascotas/crear.html",data)

def editar_mascota(request,id):
    usuario = Usuario.objects.get(usuario=request.user)
    mascota = Mascota.objects.get(id=id)

    if usuario.tipo_usuario == "CLI":
        cliente = Cliente.objects.get(usuario=request.user)
        if mascota.dueño != cliente:
            messages.error(request, "No puede modificar una mascota que no es suya")
            return redirect ("listar_mascotas")
    elif usuario.tipo_usuario not in ["REC","ADMIN"]:
        messages.error(request,"No tiene permisos para modificar mascotas")
        return redirect("inicio")
    
    if request.method == "POST":
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, "Mascota actualizada correctamente")
            return redirect("listar_mascotas")
        else:
            messages.error(request, "Error al actualizar la mascota")
    
    else:
        form= MascotaForm(instance=mascota)
    
    data = {"form":form, "mascota":mascota}
    return render(request, "mascotas/editar.html",data)

def eliminar_mascota(request, id):
    usuario = Usuario.objects.get(usuario=request.user)
    mascota = Mascota.objects.get(id=id)
    if usuario.tipo_usuario not in ["ADMIN","REC"]:
        messages.error(request, "No tiene permisos para eliminar mascotas")
        return redirect("inicio")
    
    if request.method == "POST":
        mascota.delete()
        messages.success(request, "Mascota eliminada correctamente")
        return redirect("listar_mascotas")
    data = {"mascota":mascota}
    return render(request, "mascotas/eliminar.html",data)

def listar_citas(request):
    usuario = Usuario.objects.get(usuario= request.user)
    if usuario.tipo_usuario not in ["ADMIN","REC","VET","CLI"]:
        messages.error(request,"No tiene permisos para ver las citas")
        return redirect("inicio")
    if usuario.tipo_usuario == "CLI":
        cliente = Cliente.objects.get(usuario=request.user)
        mascotas_cliente = Mascota.objects.filter(dueño=cliente)
        citas = Cita.objects.filter(mascota__in= mascotas_cliente)
    elif usuario.tipo_usuario == "VET":
        veterinario = Veterinario.objects.get(usuario= request.user)
        citas = Cita.objects.filter(veterinario=veterinario)
    else:
        citas = Cita.objects.all()
    
    data = {"citas":citas}
    return render(request, "citas/listar.html",data)

def crear_cita(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario not in ["REC","CLI"]:
        messages.error(request, "No tiene permisos para registrar citas")
        return redirect("inicio")
    if request.method == "POST":
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita programada correctamente")
            return redirect ("listar_citas")
        
        else:
            messages.error(request, "Error al registrar la cita")
    else:
        form = CitaForm()
    data = {"form":form}
    return render(request, "citas/crear.html",data)

def editar_cita(request, id):
    usuario= Usuario.objects.get(usuario=request.user)
    cita = Cita.objects.get(id=id)

    if usuario.tipo_usuario == "VET":
        veterinario = Veterinario.objects.get(usuario=request.user)
        if cita.veterinario != veterinario:
            messages.error(request, "No puede modificar una cita que no le pertenece")
            return redirect("listar_citas")
    elif usuario.tipo_usuario not in ["ADMIN","REC"]:
        messages.error(request, "No tiene permisos para modificar citas")
        return redirect("inicio")
    
    if request.method == "POST":
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita actualizada correctamente")
            return redirect("listar_citas")
        else:
            messages.error(request, "Error al actualizar la cita")
    else:
        form = CitaForm(instance=cita)
    data={"form":form, "cita":cita}
    return render(request, "citas/editar.html",data)

def eliminar_cita(request, id):
    usuario = Usuario.objects.get(usuario=request.user)
    cita = Cita.objects.get(id=id)

    if usuario.tipo_usuario not in ["ADMIN","REC"]:
        messages.error(request,"No tiene permisos para eliminar citas")
        return redirect("inicio")
    if request.method == "POST":
        cita.delete()
        messages.success(request,"Cita eliminada correctamente")
        return redirect("listar_citas")
    data = {"cita":cita}
    return render(request, "citas/eliminar.html",data)
def agendar_proxima_cita(request, consulta_id):
    consulta = Consulta.objects.get(id = consulta_id)
    if consulta.cita.veterinario.usuario != request.user:
        messages.error(request, "No tiene permisos para agendar la proxima cita")
        return redirect("listar_citas")
    if request.method == "POST":
        fecha_hora = request.POST.get("fecha_hora")
        if fecha_hora:
            cita = Cita(
                mascota = consulta.cita.mascota,
                veterinario = consulta.cita.veterinario
                fecha_hora= fecha_hora,
                estado = "PROG",
                motivo_consulta = "Proxima consulta"
                )
                
            cita.save()
            messages.success(request, "Proxima cita agendada correctamente")
            return redirect("listar_citas")
        else: messages.error(request, "Debe ingresar una fecha y hora valida")
        data = {"consulta":consulta}
        return render(request, "citas/agendar.html",data)

def listar_consultas(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario not in ["ADMIN","VET","REC"]:
        messages.error(request, "No tiene permisos para ver el historial medico")
        return redirect("inicio")
    if usuario.tipo_usuario== "VET":
        veterinario = Veterinario.objects.get(usuario=request.user)
        citas_vet = Cita.objects.filter(veterinario=veterinario)
        consultas = Consulta.objects.filter(cita__in = citas_vet)
    else:
        consultas = Consulta.objects.all()
    data = {"consultas": consultas}
    return render(request,"consultas/listar.html", data)

def crear_consulta(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario != "VET":
        messages.error(request, "No tiene permisos para registrar una consulta medica")
        return redirect("inicio")
    if request.method == "POST":
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Consulta registrada correctamente")
            return redirect("listar_consultas")
        else: 
            messages.error(request, "Error al registrar la consulta")
    else:
        form = ConsultaForm()
    data = {"form":form}
    return render(request, "consultas/crear.html",data)

def editar_consulta(request, id):
    usuario = Usuario.objects.get(usuario=request.user)
    consulta = Consulta.objects.get(id=id)
    if usuario.tipo_usuario =="VET":
        veterinario = Veterinario.objects.get(usuario=request.user)
        if consulta.cita.veterinario != veterinario:
            messages.error(request, "No puede modificar una consulta que no le pertenece")
            return redirect("listar_consultas")
    elif usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para editar consultas")
        return redirect("inicio")
    if request.method == "POST":
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "Consulta actualizada correctamente")
            return redirect("listar_consultas")
        else:
            messages.error(request,"Error al actualizar la consulta")
    else:
        form = ConsultaForm(instance=consulta)
    data = {"form":form, "consulta":consulta}
    return render(request, "consultas/editar.html",data)

def eliminar_consulta(request, id):
    usuario = Usuario.objects.get(usuario=request.user)
    consulta = Consulta.objects.get(id=id)
    if usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para eliminar consultas")
        return redirect("inicio")
    if request.method == "POST":
        consulta.delete()
        messages.success(request, "Consulta eliminada correctamente")
        return redirect("listar_consultas")
    data = {"consulta":consulta}
    return render(request, "consultas/eliminar.html", data)

def historial_medico(request, mascota_id):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario != "CLI":
        messages.error(request, "No tiene permisos para ver el historial médico de esta mascota.")
        return redirect("inicio")

    cliente = Cliente.objects.get(usuario=request.user)
    mascota = Mascota.objects.get(id=mascota_id)
    
    if mascota.dueño != cliente:
        messages.error(request, "No puede ver el historial médico de una mascota que no es suya.")
        return redirect("listar_mascotas")
    
    consultas = Consulta.objects.filter(cita__mascota=mascota)
    data = {"mascota": mascota, "consultas": consultas}
    return render(request, "consultas/historial.html", data)


def listar_medicamentos(request):
    usuario = Usuario.objects.get(usuario=request.user)
    if usuario.tipo_usuario not in ["ADMIN","VET"]:
        messages.error(request, "No tiene permisos para ver los medicamentos")
        return redirect("inicio")
    medicamentos = Medicamento.objects.all()
    data = {"medicamentos":medicamentos}
    return render(request, "medicamentos/listar.html",data)

def crear_medicamento(request):
    usuario = Usuario.objects.get(usuario=request.user)

    if usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para registrar medicamentos")
        return redirect("inicio")
    if request.method == "POST":
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicamento registrado")
            return redirect("listar_medicamentos")
        else:
            messages.error(request, "Error al registrar el medicamento")
    else:
        form = MedicamentoForm()
    data = {"form":form}
    return render(request, "medicamentos/crear.html",data)

def editar_medicamento(request, id):
    usuario = Usuario.objects.get(usuario=request.user)
    medicamento = Medicamento.objects.get(id=id)
    if usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para editar medicamentos")
        return redirect("inicio")
    if request.method == "POST":
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            messages.success(request,"Medicamento actualizado correctamente")
            return redirect("listar_medicamentos")
        else:
            messages.error(request, "Error al actualizar el medicamento")
    else:
        form = MedicamentoForm(instance=medicamento)
    data = {"form":form, "medicamento":medicamento}
    return render(request,"medicamentos/editar.html",data)
    
def eliminar_medicamento(request,id):
    usuario = Usuario.objects.get(usuario=request.user)
    medicamento = Medicamento.objects.get(id=id)
    if usuario.tipo_usuario != "ADMIN":
        messages.error(request, "No tiene permisos para eliminar medicamentos")
        return redirect("inicio")
    if request.method == "POST":
        medicamento.delete()
        messages.success(request, "Medicamento eliminado correctamente")
        return redirect("listar_medicamentos")
    data = {"medicamento": medicamento}
    return render ( request, "medicamentos/eliminar.html",data)
