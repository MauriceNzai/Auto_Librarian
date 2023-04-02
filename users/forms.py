"""
Modelling User for registration, login and logout fuctions
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """
    Models user registration 
    """
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    email = forms.EmailField()

    class Meta:
        """
        The Meta class
        """
        model = User
        fields = ['username', 'first_name', 'last_name',
                        'email', 'password1', 'password2']
