"""
URL config for the users app
"""
from django.contrib.auth import views as auth_views
from django.urls import path
from users import views as user_views

urlpatterns = [
        path('register/', user_views.register, name='register'),
        path('login/', auth_views.LoginView.as_view(
                template_name='users/login.html') , name='login'),
        path('logout/', auth_views.LogoutView.as_view(
                template_name='librarian/home.html') , name='logout'),
    ]
