from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Paciente
from .models import Consulta
from .forms import ConsultaForm

@login_required
def home(request):
    return  render (request, 'doctor_portal/home.html')

@login_required
def agenda(request):
    context = {
        'Consultas': Consulta.objects.all()
    }
    return  render (request, 'doctor_portal/agenda.html', context)

@login_required
def pacientes(request):
    context = {
        'Pacientes': Paciente.objects.all()
    }
    return  render (request, 'doctor_portal/pacientes.html', context)

@login_required
def perfil(request):
    return  render (request, 'doctor_portal/perfil.html')

@login_required
def consulta(request, Paciente_nome):
    paciente = Paciente.objects.get(nome=Paciente_nome)
    consulta_aux = paciente.consultas
    form = ConsultaForm(instance=paciente.consultas)

    if (request.method == 'POST'):
        form = ConsultaForm(request.POST, instance=consulta_aux)

        if(form.is_valid()):
            consulta_aux.save()
            return redirect('/')
        else:
            return render (request, 'doctor_portal/consulta.html', {'Paciente':paciente, 'form': form})

    else:
        return render (request, 'doctor_portal/consulta.html', {'Paciente':paciente, 'form': form})


