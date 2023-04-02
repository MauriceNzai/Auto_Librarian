"""
App configurations
"""
from django.apps import AppConfig


class LibrarianConfig(AppConfig):
    """
    configures the app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'librarian'
