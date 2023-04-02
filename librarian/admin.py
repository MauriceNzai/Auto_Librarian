"""
Registers models
"""
from django.contrib import admin
from .models import Book, Issue, Member, ReturnBook

# Register your models here.
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Issue)
admin.site.register(ReturnBook)
