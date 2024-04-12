from rest_framework import serializers
from .models import CustomUser, Appointment, Document

class CustomUserSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = ('patient_id', 'full_name', 'age', 'weight', 'height', 'gender',
                  'dietary_restrictions', 'medical_observation', 'nutritionist_observation',
                  'personal_trainer_observation', 'psychologist_observation')

class AppointmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        source='patient',
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        model = Appointment
        fields = ('id', 'patient_id', 'professional_id', 'profession', 'time')
        read_only_fields = ('id',)

class DocumentSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(
        source='patient',
        queryset=CustomUser.objects.all()
    )

    class Meta:
        model = Document
        fields = ('id', 'patient_id', 'professional_id', 'profession', 'object_tag')
        read_only_fields = ('id',)

class CustomPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'full_name')  # Adjust 'full_name' as needed

class CustomAppointmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='patient.full_name', read_only=True)
    datetime = serializers.DateTimeField(source='time')

    class Meta:
        model = Appointment
        fields = ('name', 'datetime')

class CustomPatientDetailSerializer(serializers.ModelSerializer):
    dietary_restrictions = serializers.CharField()
    medical_observation = serializers.CharField()
    nutritionist_observation = serializers.CharField()
    personal_trainer_observation = serializers.CharField()
    psychologist_observation = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'age', 'weight', 'height', 'gender',
                  'dietary_restrictions', 'medical_observation', 'nutritionist_observation',
                  'personal_trainer_observation', 'psychologist_observation')

class CustomDocumentSerializer(serializers.ModelSerializer):
    documentId = serializers.CharField(source='id')
    url = serializers.CharField(source='object_tag')

    class Meta:
        model = Document
        fields = ('documentId', 'profession', 'url')

class CustomObservationSerializer(serializers.Serializer):
    observation = serializers.CharField()

class CustomDocumentPostSerializer(serializers.ModelSerializer):
    documentId = serializers.CharField(write_only=True)  # Accept documentId as input, not as a model field
    url = serializers.URLField(write_only=True)          # Accept URL as input

    class Meta:
        model = Document
        fields = ('documentId', 'url')

    def create(self, validated_data):
        # Construct the object_tag from provided data
        object_tag = json.dumps({
            "documentId": validated_data['documentId'],
            "url": validated_data['url']
        })
        # Create the Document instance with the serialized object_tag
        document = Document(object_tag=object_tag)
        document.save()
        return document