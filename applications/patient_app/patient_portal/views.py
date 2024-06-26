from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.utils import timezone
from datetime import datetime
import json
import boto3
import tempfile
import os
from django.utils.timezone import now
from dotenv import load_dotenv

from .forms import CustomUserCreationForm, EditUserInfoForm, AppointmentForm

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets

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
    professionals = get_professionals()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment created successfully.')
            return HttpResponseRedirect('/appointments')
        else:
            print(form.errors)
            messages.error(request, 'Failed to create appointment.')
            return render(request, 'services/appointments.html', {'professionals': professionals})
    else:
        return render(request, 'services/appointments.html', {'professionals': professionals})

def agenda(request):
    # Fetch appointments for the logged-in user
    user_appointments = Appointment.objects.filter(
        patient=request.user,
        time__gte=timezone.now()  # Filter for future appointments
    ).order_by('time')

    # Format appointments for FullCalendar
    events = [
        {
            'title': f'Consulta com {appointment.professional_name}',  # Updated title
            'start': appointment.time.isoformat(),  # Maintain ISO format for FullCalendar compatibility
            'description': f'Consulta com {appointment.profession}',
            'allDay': False  # Ensure this is false if you use specific times
        } for appointment in user_appointments
    ]
    # Pass events data as JSON
    return render(request, 'services/agenda.html', {'events': json.dumps(events)})

def consultations(request):
    current_user = request.user
    current_date = now().date()
    appointments = Appointment.objects.filter(patient=current_user).order_by('time')
    
    for appointment in appointments:
        # Comparing dates directly, assuming 'time' is a datetime field
        appointment.can_access = (appointment.time.date() == current_date)
    
    context = {
        'appointments': appointments,
    }
    
    return render(request, 'services/consultations.html', context)

def documents(request):
    # Fetch documents for the logged-in user and organize them by profession
    user_documents = Document.objects.filter(patient=request.user).order_by('profession')
    
    documents_by_profession = {
        'Nutricionais': [],
        'Médicos': [],
        'Psicólogicos': [],
        'do Personal Trainer': []
    }

    for doc in user_documents:
        # Extract and assign document details
        doc_details = get_document_details(doc)
        profession_key = ''  # Determine the key for the profession
        if doc.profession == 'nutritionist':
            profession_key = 'Nutricionais'
        elif doc.profession == 'medic':
            profession_key = 'Médicos'
        elif doc.profession == 'psychologist':
            profession_key = 'Psicólogicos'
        elif doc.profession == 'personal trainer':
            profession_key = 'do Personal Trainer'
        
        if profession_key:
            
            documents_by_profession[profession_key].append({
                'id': doc.id,
                'title': doc_details['key'],
                'url': doc_details['url'],
                'description': doc_details['description']
            })

    return render(request, 'services/documents.html', {'documents': documents_by_profession})

def download_document(request, title):
    # Load environment variables
    load_dotenv()

    # Initialize S3 client
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION_NAME")
    )

    # Extract a safe file name
    safe_title = title.split('/')[-1]

    try:
        # Generate a pre-signed URL for the S3 object
        response = s3.generate_presigned_url('get_object',
                                            Params={'Bucket': 'vitalink',
                                                    'Key': title},
                                            ExpiresIn=3600)  # Link expires in 1 hour

        # Redirect user to the pre-signed URL for direct file download
        return redirect(response)
    except Exception as e:
        messages.error(request, f"Failed to download document: {str(e)}")
        # Log the error and return an error message
        print(f"Error generating pre-signed URL: {str(e)}")
        return HttpResponse(f"Failed to generate download link: {str(e)}", status=500)
    
def profile(request):
    return render(request, 'services/profile.html') 

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditUserInfoForm(request.POST, instance=request.user)
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
    
#UTILS

def professional_union():
    urls = [
        'http://ec2-54-152-228-191.compute-1.amazonaws.com:8000/users/time_slots/', #nutritionist
        'http://ec2-54-233-193-209.sa-east-1.compute.amazonaws.com:8000/api/users/time_slots/', #personal trainer
        'http://ec2-15-229-233-111.sa-east-1.compute.amazonaws.com:8000/api/users/time_slots/', # psychologist
        'http://ec2-54-207-151-203.sa-east-1.compute.amazonaws.com:8000/api/users/time_slots/', # medic
    ]
    professional_types = ['Nutricionista', 'Personal Trainer', 'Psicólogo', 'Médico']
    all_professionals = []

    # Function to translate day numbers to day names
    def translate_days(days):
        day_mapping = {
            0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sab", 6: "Dom"
        }
        return [day_mapping.get(day) for day in days]

    # Loop through each API endpoint
    for url, profession in zip(urls, professional_types):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP error codes
            professionals = response.json()

            # Format each professional's data
            for professional in professionals:
                professional['type'] = profession
                professional['days_available'] = translate_days(professional['days_available'])
            all_professionals.extend(professionals)
        except requests.RequestException as e:
            print(f"Failed to fetch data from {url}: {str(e)}")

    return all_professionals

def get_professionals():
    professionals = professional_union()
    url_mappings = {
        'Nutricionista': 'http://ec2-54-152-228-191.compute-1.amazonaws.com:8000/time_slots/', # Nutricionista
        'Personal Trainer': 'http://ec2-54-233-193-209.sa-east-1.compute.amazonaws.com:8000/api/time_slots/', # Personal Trainer
        'Psicólogo': 'http://ec2-15-229-233-111.sa-east-1.compute.amazonaws.com:8000/api/time_slots/', # Psicólogo
        'Médico': 'http://ec2-54-207-151-203.sa-east-1.compute.amazonaws.com:8000/api/time_slots/', # Médico
    }
    # Function to correct and verify time format
    def fix_time_format(time_string):
        try:
            # Ensure the time string is complete with seconds
            if len(time_string) == 16:  # 'YYYY-MM-DDTHH:MM'
                time_string += ':00'
            dt = datetime.fromisoformat(time_string)  # Corrected to datetime.datetime.fromisoformat
            return dt.isoformat()
        except ValueError:
            return None

    # Iterate through each professional and fetch their time slots
    for professional in professionals:
        professional_type = professional['type']
        professional_id = professional['id']
        base_url = url_mappings.get(professional_type, '')
        time_slots_url = f"{base_url}{professional_id}/"

        try:
            response = requests.get(time_slots_url)
            response.raise_for_status()
            time_slots = response.json()

            # Filter out past or booked time slots
            filtered_slots = []
            for slot in time_slots:
                corrected_slot = fix_time_format(slot)
                if corrected_slot:
                    slot_time = timezone.make_aware(datetime.fromisoformat(corrected_slot))
                    # Check against current time and booked appointments
                    if slot_time > timezone.now():
                        # Check if the slot is not already booked
                        if not Appointment.objects.filter(professional_id=professional_id, time=slot_time).exists():
                            filtered_slots.append(corrected_slot)

            professional['time_slots'] = filtered_slots
        except requests.RequestException as e:
            print(f"Failed to fetch time slots for {professional['name']} ({professional_type}): {str(e)}")
            professional['time_slots'] = []

    return professionals

def get_document_details(document):
    try:
        # Assuming object_tag is a JSON field with 'url' and 'description' keys
        details = json.loads(document.object_tag)
        return {
            'url': details.get('url', 'No url available.'),
            'description': details.get('description', 'No description available.'),
            'key': details.get('key', 'Unnamed Document')
        }
    except json.JSONDecodeError:
        return {
            'url': '',
            'description': 'Invalid document details.',
            'key': 'Unnamed Document'
        }
    
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

    profession_mapping = {
        'nutritionist': 'Nutricionista',
        'psychologist': 'Psicólogo',
        'personal_trainer': 'Personal Trainer',
        'medic': 'Médico'
    }

    @swagger_auto_schema(
        method='get',
        responses={200: CustomPatientSerializer(many=True)},
        operation_description="Retrieve a list of patients for a given professional."
    )
    @action(detail=False, url_path='(?P<profession>[^/.]+)/(?P<professional_id>\d+)/patients')
    def professional_patients(self, request, profession, professional_id):
        profession_in_db = self.profession_mapping.get(profession.lower())
        print(profession_in_db)
        try:
            # Use the correct related_name 'patient_appointments' in the query
            patients = CustomUser.objects.filter(
                patient_appointments__professional_id=professional_id,
                patient_appointments__profession=profession_in_db
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
        # Map the URL profession parameter to the database value
        profession_in_db = self.profession_mapping.get(profession.lower())

        # If the profession is not in the mapping, return a 404 response
        if not profession_in_db:
            return Response({'error': 'Profession not found'}, status=404)

        appointments = Appointment.objects.filter(
            professional_id=professional_id,
            profession=profession_in_db
        )
        for appointment in appointments:
            appointment.time = appointment.time+timezone.timedelta(hours=3)
        
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
                    "key": serializer.validated_data['key'], 
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
