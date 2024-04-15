from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, EditUserInfoForm

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import generics, viewsets

from .models import CustomUser, Appointment, Document
from .serializers import (CustomUserSerializer, AppointmentSerializer, DocumentSerializer, 
                         CustomPatientSerializer, CustomAppointmentSerializer, CustomPatientDetailSerializer,
                         CustomDocumentSerializer, CustomObservationSerializer, CustomDocumentPostSerializer)

from drf_yasg.utils import swagger_auto_schema

def index(request):
    return render(request, 'services/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please log in.")
            return HttpResponseRedirect('/')
        else:
            print("Form Errors:", form.errors)
            messages.error(request, "Registration failed. Please correct the errors below and try again.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def dashboard(request):
    return render(request, 'services/dashboard.html')

def appointments(request):
    return render(request, 'services/appointments.html')

def agenda(request):
    return render(request, 'services/agenda.html')

def consultations(request):
    return render(request, 'services/consultations.html')

def documents(request):
    return render(request, 'services/documents.html')

def profile(request):
    return render(request, 'services/profile.html') 

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditUserInfoForm(request.POST, instance=request.user)
        print("POST data:", request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return HttpResponseRedirect('/profile')  # Directly using the URL path
        else:
            # Iterate through form errors to print and display them
            for field, errors in form.errors.items():
                for error in errors:
                    error_message = f"Error in {field}: {error}"
                    # Print the error message to the console
                    print(error_message)
                    # Add error message to Django's messaging framework
                    messages.error(request, error_message)
            
            return HttpResponseRedirect('/profile')  # Redirect back to the profile, adjust if needed
    else:
        return HttpResponseRedirect('/profile')  # Redirect if not POST

#API CALLS (URRESTRICTED ACCESS TO SIMPLIFY THE PROCESS)

#CRUD ENDPOINTS FOR DEVELOPEMENT PURPOSES
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

#API CALLS TO FEED OTHER APPLICATIONS

class CustomProfessionalViewSet(ViewSet):

    @swagger_auto_schema(
        method='get',
        responses={200: CustomPatientSerializer(many=True)},
        operation_description="Retrieve a list of patients for a given professional."
    )
    @action(detail=False, url_path='(?P<profession>[^/.]+)/(?P<professional_id>\d+)/patients')
    def professional_patients(self, request, profession, professional_id):
        try:
            # Use the correct related_name 'patient_appointments' in the query
            patients = CustomUser.objects.filter(
                patient_appointments__professional_id=professional_id,
                patient_appointments__profession=profession
            ).distinct()
            serializer = CustomPatientSerializer(patients, many=True)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Patients for the given professional and profession not found'}, status=404)
        except Exception as e:
            # Log the error for debugging purposes
            # logger.error('Unexpected error occurred', exc_info=e)
            return Response({'error': str(e)}, status=500)

    @swagger_auto_schema(
        method='get',
        responses={200: CustomAppointmentSerializer(many=True)},
        operation_description="Retrieve appointments for a given professional."
    )
    @action(detail=False, url_path='(?P<profession>[^/.]+)/(?P<professional_id>\d+)/appointments')
    def professional_appointments(self, request, profession, professional_id):
        appointments = Appointment.objects.filter(professional_id=professional_id, profession=profession)
        serializer = CustomAppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

class CustomPatientViewSet(ViewSet):

    @swagger_auto_schema(
        method='get',
        responses={200: CustomPatientDetailSerializer()},
        operation_description="Retrieve details for a specific patient."
    )
    @action(detail=False , methods=['get'], url_path='(?P<patient_id>\d+)/details')
    def patient_details(self, request, patient_id=None):
        patient = CustomUser.objects.get(pk=patient_id)
        serializer = CustomPatientDetailSerializer(patient)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='get',
        responses={200: CustomDocumentSerializer(many=True)},
        operation_description="Retrieve documents for a specific patient by professional."
    )
    @action(detail=False, methods=['get'], url_path='(?P<patient_id>\d+)/(?P<profession>[^/.]+)/(?P<professional_id>\d+)/getdocuments')
    def patient_documents(self, request, patient_id=None, profession=None, professional_id=None):
        documents = Document.objects.filter(patient_id=patient_id, professional_id=professional_id, profession=profession)
        serializer = CustomDocumentSerializer(documents, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='post',
        request_body=CustomObservationSerializer,
        responses={200: CustomObservationSerializer()},
        operation_description="Post an observation for a specific patient and professional."
    )
    @action(detail=False, methods=['post'], url_path='(?P<patient_id>\d+)/(?P<profession>[^/.]+)/(?P<professional_id>\d+)/observation')
    def post_observation(self, request, patient_id=None, profession=None, professional_id=None):
        serializer = CustomObservationSerializer(data=request.data)
        if serializer.is_valid():
            observation = serializer.validated_data['observation']
            patient = CustomUser.objects.get(pk=patient_id)
            if profession == 'nutritionist':
                patient.nutritionist_observation = observation
            elif profession == 'medic':
                patient.medical_observation = observation
            elif profession == 'personal trainer':
                patient.personal_trainer_observation = observation
            elif profession == 'psychologist':
                patient.psychologist_observation = observation
            patient.save()
            return Response({'status': 'observation updated'})
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        method='post',
        request_body=CustomDocumentPostSerializer,
        responses={200: CustomDocumentPostSerializer()},
        operation_description="Post a new document with its ID and URL for a specific patient and professional."
    )
    @action(detail=False, methods=['post'], url_path='(?P<patient_id>\d+)/(?P<profession>[^/.]+)/(?P<professional_id>\d+)/postdocuments')
    def post_documents(self, request, patient_id, profession, professional_id):
        serializer = CustomDocumentPostSerializer(data=request.data, context={
            'patient_id': patient_id,
            'profession': profession,
            'professional_id': professional_id
        })
        if serializer.is_valid():
            try:
                document = serializer.save()
                return Response({
                    "documentId": serializer.validated_data['documentId'], 
                    "url": serializer.validated_data['url'],
                    "message": "Document created successfully"
                }, status=201)
            except IntegrityError as e:
                # Handle specific database errors e.g., missing required fields
                return Response({'error': 'Failed to create document due to an integrity error.'}, status=400)
            except Exception as e:
                # Handle any other exception that wasn't anticipated
                return Response({'error': str(e)}, status=500)
        else:
            # Handle validation errors
            return Response(serializer.errors, status=400)


# 1)
# get /professional/{profession}/{professional_id}/patients
# [
#   {
#     "id": 1,
#     "name": "Alice"
#   },
#   {
#     "id": 2,
#     "name": "Breno"
#   }
# ]


# 2)
# get /professional/{profession}/{professional_id}/appointments
# [
#   {
#     "name": "Alice",
#     "datetime": "2024-04-12 09:00:00"
#   },
#   {
#     "name": "Breno",
#     "datetime": "2024-04-13 10:00:00"
#   }
# ]


# 3) 
# get /patient/{patient_id}/details
# {
#   "id": 1,
#   "name": "Alice",
#   "age": 29,
#   "weight": 60, 
#   "height": 165, 
#   "gender": "Female",
#   "dietaryRestrictions": "None",
#   "notes": [
#     {
#       "profession": "personal trainer",
#       "content": "Needs follow-up"
#     },
#     {
#       "profession": "psicologist",
#       "content": "Medication adjusted"
#     }
#   ]
# }

# 4)
# get /patient/{patient_id}/{profession}/{professional_id}/documents
# [
#   {
#     "documentId": "file123",
#     "profession": "nutritionist",
#     "url": "https://s3.example.com/bucket/file123",
#     "uploaded": "2024-03-01"
#   },
#   {
#     "documentId": "file456",
#     "profession": "personal trainer",
#     "url": "https://s3.example.com/bucket/file456",
#     "uploaded": "2024-03-02"
#   }
# ]

# 5)
# post /patient/{patient_id}/{profession}/{professional_id}/observation
# {
#   "observation": "Patient shows signs of improvement after treatment."
# }


# 6)
# post /patient/{patient_id}/{profession}/{professional_id}/documents
# {
#   "metadata": {
#     "documentId": "file789",
#     "url": "https://s3.example.com/bucket/file789",
#   }
# }