from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='doctor_portal-home'),
    path('agenda/', views.agenda, name='doctor_portal-agenda'),
    path('pacientes/', views.pacientes, name='doctor_portal-pacientes'),
    path('perfil/', views.perfil, name='doctor_portal-perfil'), 
    path('consulta/<str:Paciente_nome>/', views.consulta, name='doctor_portal-consulta'),
]
