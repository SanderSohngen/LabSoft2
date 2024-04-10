from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import forms


class CustomUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm):
        model = User
        fields = forms.UserCreationForm.Meta.fields + ('email','first_name','last_name',)
