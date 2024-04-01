from django.shortcuts import render

def login(request):
    return render(request, 'auth/login.html')

def register(request):
    return render(request, 'auth/register.html')

def dashboard(request):
    return render(request, 'services/dashboard.html')
