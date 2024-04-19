from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Appointment

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    
    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        # Set the username to be the same as the email
        user.username = self.cleaned_data["email"]

        full_name = self.cleaned_data["full_name"].split()
        user.first_name = full_name[0]
        if len(full_name) > 1:
            user.last_name = ' '.join(full_name[1:])  # Join the remaining strings as last name
        
        if commit:
            user.save()
        return user

class EditUserInfoForm(forms.ModelForm):
    full_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Full Name')}),
        label=_('Full Name')
    )
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('Age')}),
        label=_('Age')
    )
    gender = forms.ChoiceField(
        required=False,
        choices=CustomUser.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Gender')
    )
    weight = forms.DecimalField(
        required=False,
        max_digits=5, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('Weight (kg)')}),
        label=_('Weight (kg)')
    )
    height = forms.DecimalField(
        required=False,
        max_digits=5, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('Height (cm)')}),
        label=_('Height (cm)')
    )
    dietary_restrictions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Dietary Restrictions')}),
        label=_('Dietary Restrictions')
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'age', 'gender', 'weight', 'height', 'dietary_restrictions']

    def __init__(self, *args, **kwargs):
        super(EditUserInfoForm, self).__init__(*args, **kwargs)
        if self.instance:
            # Combine first and last name into full_name field's initial value
            self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}"

    def save(self, commit=True):
        user = super().save(commit=False)
        # Split the full name into first and last names
        full_name_parts = self.cleaned_data['full_name'].strip().split()
        user.first_name = full_name_parts[0]
        if len(full_name_parts) > 1:
            user.last_name = ' '.join(full_name_parts[1:])
        else:
            user.last_name = ''  # Clear the last name if full_name doesn't include it

        if commit:
            user.save()
        return user

class AppointmentForm(forms.ModelForm):
    time_slot = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M:%SZ'])

    class Meta:
        model = Appointment
        fields = ['patient', 'professional_id', 'professional_name', 'profession', 'time_slot']

    def clean_time_slot(self):
        time_slot = self.cleaned_data.get('time_slot')
        if time_slot:
            return time_slot
        else:
            raise forms.ValidationError("This field is required.")

    def save(self, commit=True):
        instance = super(AppointmentForm, self).save(commit=False)
        instance.time = self.cleaned_data.get('time_slot')
        if commit:
            instance.save()
        return instance