from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    # Custom fields
    full_name = models.CharField(max_length=100, null=True, verbose_name=_('Full Name'))
    account_type = models.CharField(max_length=12, choices=ACCOUNT_TYPE_CHOICES, verbose_name=_('Account Type'))
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Age'))
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True, verbose_name=_('Gender'))
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Weight (kg)'))
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_('Height (cm)'))
    dietary_restrictions = models.TextField(null=True, blank=True, verbose_name=_('Dietary Restrictions'))
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True, verbose_name=_('Profile Picture'))

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'account_type']

    def __str__(self):
        return self.email