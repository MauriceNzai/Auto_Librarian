"""
Has all the models representing the database tables
"""
from datetime import datetime, timedelta
from django.db import models
from django.urls import reverse

class Book(models.Model):
    """
    Models a book to store all book information
    """
    book_title = models.CharField(max_length=100, default='')
    author_name = models.CharField(max_length=100, default='')
    isbn_no = models.CharField('ISBN', max_length=50, default='')
    subject = models.CharField(max_length=20, default='')
    total_copies = models.PositiveIntegerField(default=0)
    available_copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        """
        Returns readable string
        """
        return self.book_title

    def get_absolute_url(self):
        """
        Overrides the get_absolute_url function
        """
        return reverse('book-detail', kwargs={'pk': self.pk})


class Member(models.Model):
    """
    Models the library member to store information of a borrower
    """
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    id_no = models.CharField(max_length=50, default='')
    contact_no = models.CharField(max_length=15, default='')
    email_id = models.EmailField(max_length=50, default='')
    no_of_issued_books = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        """
        Overrides get_absolute_url method
        """
        return reverse('member-detail', kwargs={'pk': self.pk})


# Issue model
def get_expected_return_date():
    """
    returns expected due date of borrowed book
    """
    return datetime.today() + timedelta(days=30)

class Issue(models.Model):
    """
    Models the book issue transactioon
    """
    member_name = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=datetime.today)
    expected_return_date = models.DateField(
            default=get_expected_return_date)

    def __str__(self):
        return self.book.book_title + ' issued for ' + self.member_name.first_name +\
                ' ' + self.member_name.last_name


#Return book and transaction history model
class ReturnBook(models.Model):
    """
    Models the return book transaction
    """
    actual_return_date = models.DateField(default=datetime.today)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member_name = models.ForeignKey(Member, on_delete=models.CASCADE)
    fine_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.book.book_title + ' is returned by ' + self.member_name.first_name +\
                ' ' + self.member_name.last_name
