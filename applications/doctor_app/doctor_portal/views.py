from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return  render (request, 'doctor_portal/home.html')

def agenda(request):
    return  render (request, 'doctor_portal/agenda.html')

def pacientes(request):
    return  render (request, 'doctor_portal/pacientes.html')

def perfil(request):
    return  render (request, 'doctor_portal/perfil.html')
