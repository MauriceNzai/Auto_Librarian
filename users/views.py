"""
Holds all the views for the app
"""
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from . forms import UserRegisterForm

# Create your views here.
def register(request):
    """
    user registration view
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created successfully')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})
