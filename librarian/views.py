"""
All the view functions here
"""

from datetime import datetime, date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from .models import Book, Member, Issue, ReturnBook
from .forms import IssueForm, ReturnBookForm

# books views start here
def home(request):
    return render(request, 'librarian/home.html', {'title': 'Home'})

def library(request):
    context = {
	'books': Book.objects.all()
}
    return render(request, 'librarian/book-list.html', context)

def bookTipMsg(request):
    return messages.info(request, 'Click the Book title to view book details')

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'librarian/book-list.html'
    context_object_name = 'books'
    ordering = ['-id']
    paginate_by = 10

class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book

class AddBookView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Book
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return 'Tip: Book is added to the library go and check it out!!!'

class UpdateBookView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return 'Tip: Book details are updated!!!'

class DeleteBookView(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = '/book-list/'

@login_required
def searchBooks(request):
    query = request.GET['query']

    if len(query) > 150 or len(query) == 0:
        books = Book.objects.none()
    else:
        booksbook_title = Book.objects.filter(book_title__icontains = query)
        booksauthor_name = Book.objects.filter(author_name__icontains = query)
        bookssubject = Book.objects.filter(subject__icontains=query)
        books = booksbook_title.union(booksauthor_name, bookssubject)

        if books.count() == 0:
            messages.warning(request, f'No records found, please redefine your query')

        params = {
                'books': books,
		'title': 'Search Books',
		'query': query
	}

        return render(request, 'librarian/search_books.html', params)


#views relating to members start here

class MemberListView(LoginRequiredMixin, ListView):
    model = Member
    template_name = 'librarian/members.html'
    context_object_name = 'members'
    ordering = ['-id']
    paginate_by = 10


class MemberDetailView(LoginRequiredMixin, DetailView):
    model = Member


class AddMemberView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Member
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
    	return 'Tip: Member data is added successfully'


class UpdateMemberView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    fields = '__all__'

    def form_valid(self, form):
    	return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return 'Tip: Member details updated successfully'


class DeleteMemberView(LoginRequiredMixin, DeleteView):
    model = Member
    success_url = '/members/'


@login_required
def searchMember(request):
    query = request.GET['query']

    if len(query) > 150 or len(query) == 0:
        members = Member.objects.none()

    else:
        member_fname = Member.objects.filter(first_name__icontains = query)
        member_lname = Member.objects.filter(last_name__icontains = query)
        member_id_no = Member.objects.filter(id_no__icontains = query)
        member_contact = Member.objects.filter(contact_no__icontains = query)
        member = member_fname.union(member_lname, member_id_no, member_contact)

        if members.count() == 0:
            messages.warning(request, f'No record found, please redefine your query')

    params = {
            'members': members,
	    'title': 'Search Members',
	    'query': query
	}

    return render(request, 'librarian/search_members.html', params)


# basic library functionality start here

@login_required
def IssueBook(request, pk):
    if request.method == 'POST':
        obj = Member.objects.get(id=pk)
        form = IssueForm(request.POST)

        if form.is_valid():
            book = form.cleaned_data['book']
            member = Member.objects.get(id=obj.id)

            bookObj = Book.objects.get(book_title=book)
            if member.no_of_issued_books > 10:
                messages.warning(request, 'Maximum number of borrowed books reached.')
                form = IssueForm()

            else:
                if bookObj.available_copies == 0:
                    messages.info(request, 'Sorry!! Books not available.')
                    form = IssueForm()

                else:
                    form.save()
                    books = Book.objects.get(book_title=book)
                    member.no_of_issued_books = member.no_of_issued_books + 1
                    books.available_copies = books.available_copies - 1
                    member.save()
                    books.save()
                    messages.success(request, books.book_title + ' is issued to ' + member.first_name)
                    return redirect('currently-issued')
                
    else:
        form = IssueForm()

        context = {
                'form': form,
		'title': 'Issue book',
		'fname': Member.objects.get(id=pk).first_name,
		'lname': Member.objects.get(id=pk).last_name
            }

        return render(request, 'librarian/issue_form.html', context)


@login_required
def currentlyIssued(request):
    context = {
            'issued': Issue.objects.all().order_by('-id'),
	    'title': 'Issued Books'
	}

    return render(request, 'librarian/currently_issued.html', context)


class CurrentlyIssuedView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'librarian/currently_issued.html'
    context_object_name = 'issued'
    ordering = ['-id']
    paginate_by = 10



def calculate_penalty(issue):
    return (date.today() - issue.expected_return_date).days * 50


@login_required
def returnBook(request, pk):
    if request.method == 'POST':
        obj = get_object_or_404(Issue, id=pk)

        fine = 0
        d1 = date.today()
        d2 = obj.expected_return_date
        diff_date = d2.day - d1.day
        if diff_date > 0:
            fine = diff_date*50

        book = Book.objects.get(book_title=obj.book)
        book.available_copies = book.available_copies + 1
        book.save()

        fname = obj.member_name.first_name

        member = Member.objects.get(first_name=fname)
        member.no_of_issued_books = member.no_of_issued_books - 1
        member.save()

        initial_dict = {
            'book' : obj.book,
            'member_name': obj.member_name,
            'actual_return_date': datetime.today,
            'fine_amount': fine,
        }

        form = ReturnBookForm(request.POST or None, initial=initial_dict)

        Issue.objects.get(id=obj.id).delete()
        
        if form.is_valid():
            form.save()
            messages.success(request, 'You have returned the book')
            return redirect('returned-book')

    else:
        form = ReturnBookForm()

        context = {
            'form': form
        }
        return render(request, 'librarian/return_book_form.html', context)

@login_required
def TransactionandReturnBook(request):
    context = {
            'returns':  ReturnBook.objects.all().order_by('-id'),
	    'title': 'Returned Books and Transaction History'
	}

    return render(request, 'librarian/return_and_transaction.html', context)
