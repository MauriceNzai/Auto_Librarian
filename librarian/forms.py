"""
All the forms for data collection
"""
from django import forms
from . models import Issue, ReturnBook


class IssueForm(forms.ModelForm):
    """
    The issue book form
    """
    class Meta:
        """
        Meta model
        """
        model = Issue
        fields = [
                'member_name',
                'book'
                ]


class ReturnBookForm(forms.ModelForm):
    """
    The return book form
    """
    class Meta:
        """
        Meta class
        """
        model = ReturnBook
        fields = [
                'actual_return_date',
                'book',
                'member_name',
                'fine_amount'
        ]
