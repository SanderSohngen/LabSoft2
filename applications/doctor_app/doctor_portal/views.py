from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Paciente
from .models import Consulta
from .forms import ConsultaForm

def home(request):
    return  render (request, 'doctor_portal/home.html')

def agenda(request):
    context = {
        'Consultas': Consulta.objects.all()
    }
    return  render (request, 'doctor_portal/agenda.html', context)

def pacientes(request):
    context = {
        'Pacientes': Paciente.objects.all()
    }
    return  render (request, 'doctor_portal/pacientes.html', context)

def perfil(request):
    return  render (request, 'doctor_portal/perfil.html')

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


