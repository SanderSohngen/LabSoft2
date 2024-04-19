from rest_framework import serializers
from .models import CustomUser, Appointment, Document
import json

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
    name = serializers.CharField(source='full_name')
    class Meta:
        model = CustomUser
        fields = ('id', 'name') 

class CustomAppointmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='patient.full_name')
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
    name = serializers.CharField(source='full_name', read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'age', 'weight', 'height', 'gender',
                  'dietary_restrictions', 'medical_observation', 'nutritionist_observation',
                  'personal_trainer_observation', 'psychologist_observation')

class CustomDocumentSerializer(serializers.ModelSerializer):
    key = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ('key',)

    def get_key(self, obj):
        # Parse the JSON stored in object_tag and return the documentId
        if obj.object_tag:
            object_tag = json.loads(obj.object_tag)
            return object_tag.get('key')
        return None

    
class CustomObservationSerializer(serializers.Serializer):
    observation = serializers.CharField()

class CustomDocumentPostSerializer(serializers.ModelSerializer):
    key = serializers.CharField(write_only=True)

    class Meta:
        model = Document
        fields = ('key',)

    def create(self, validated_data):
        object_tag = json.dumps({
            "key": validated_data['key'],
        })

        document = Document(
            patient_id=self.context['patient_id'], 
            profession=self.context['profession'], 
            professional_id=self.context['professional_id'],
            object_tag=object_tag
        )
        document.save()
        return document