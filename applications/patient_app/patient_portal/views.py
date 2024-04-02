from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import CustomUserCreationForm

def index(request):
    return render(request, 'services/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # The form is valid and can be saved.
            user = form.save()
            # Optionally, you might want to log the user in directly after registration:
            # login(request, user)

            # Redirect the user to a different page, e.g., the login page or home page.
            messages.success(request, "Registration successful. Please log in.")
            return HttpResponseRedirect('/')
        else:
            # Form validation failed, print errors to the console for debugging.
            print("Form Errors:", form.errors)
            # Optionally, display form errors using Django messages framework or directly in the template.
            messages.error(request, "Registration failed. Please correct the errors below and try again.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    else:
        form = CustomUserCreationForm()

    # Render the registration form with any validation errors.
    return render(request, 'registration/register.html', {'form': form})

def dashboard(request):
    return render(request, 'services/dashboard.html')

def appointments(request):
    return render(request, 'services/appointments.html')

def consultations(request):
    return render(request, 'services/consultations.html')

def documents(request):
    return render(request, 'services/documents.html')

def profile(request):

    context = {
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'account_type' : request.user.account_type,
    }

    return render(request, 'services/profile.html', context) 
