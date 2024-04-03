from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('appointments/', views.appointments, name='appointments'),
    path('agenda/', views.agenda, name='agenda'),
    path('consultations/', views.consultations, name='consultations'),
    path('documents/', views.documents, name='documents'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
] 