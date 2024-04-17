from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views
from .views import CustomUserViewSet, AppointmentViewSet, DocumentViewSet, CustomProfessionalViewSet, CustomPatientViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'professionals', CustomProfessionalViewSet, basename='professionals')
router.register(r'patients', CustomPatientViewSet, basename='patients')

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('appointments/', views.appointments, name='appointments'),
    path('agenda/', views.agenda, name='agenda'),
    path('consultations/', views.consultations, name='consultations'),
    path('documents/', views.documents, name='documents'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    re_path(r'^documents/download/(?P<title>.+)/$', views.download_document2, name='download_document'),
    path('api/', include(router.urls)),
]


