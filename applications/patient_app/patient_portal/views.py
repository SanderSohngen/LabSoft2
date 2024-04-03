from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from .forms import EditUserInfoForm

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