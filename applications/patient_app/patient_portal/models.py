from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomUser(AbstractUser):
    # Define choices for account type and gender
    ACCOUNT_TYPE_CHOICES = [
        ('professional', 'Professional'),
        ('patient', 'Patient'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Full Name'))
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Age'))
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Weight (kg)'))
    height = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Height (cm)'))
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True, verbose_name=_('Gender'))
    dietary_restrictions = models.TextField(null=True, blank=True, verbose_name=_('Dietary Restrictions'))
    medical_observation = models.TextField(null=True, blank=True, verbose_name=_('Medical Observation'))
    nutritionist_observation = models.TextField(null=True, blank=True, verbose_name=_('Nutritionist Observation'))
    personal_trainer_observation = models.TextField(null=True, blank=True, verbose_name=_('Personal Trainer Observation'))
    psychologist_observation = models.TextField(null=True, blank=True, verbose_name=_('Psychologist Observation'))

    # Override inherited fields to fix reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )

    # Ensure email is unique and used for login
    email = models.EmailField(_('email address'), unique=True)

    # Setting the email field as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'full_name', 'age', 'weight', 'height', 'gender']

    def __str__(self):
        return self.email
    
class Appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments', verbose_name=_('Patient'))
    professional_id = models.IntegerField(verbose_name=_('Professional ID'))
    professional_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Professional Name'))
    profession = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Profession'))
    time = models.DateTimeField(null=True, blank=True, verbose_name=_('Time'))

    def __str__(self):
        return f"Appointment for {self.patient.full_name} with professional ID {self.professional_id} on {self.time}"

class Document(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_documents', verbose_name=_('Patient'))
    professional_id = models.IntegerField(verbose_name=_('Professional ID'))
    profession = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Profession'))
    object_tag = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Object Tag'))  # Descriptive tag for the document

    def __str__(self):
        return f"Document for {self.patient.full_name} by professional ID {self.professional_id}"