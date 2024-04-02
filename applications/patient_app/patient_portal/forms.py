from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

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
    account_type = forms.ChoiceField(
        choices=[('professional', 'Professional'), ('patient', 'Patient')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2', 'account_type')
    
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