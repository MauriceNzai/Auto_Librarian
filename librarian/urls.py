"""
All urls here
"""
from django.urls import path
from . views import BookListView, BookDetailView, AddBookView, UpdateBookView, DeleteBookView
from . views import MemberListView, MemberDetailView, AddMemberView, UpdateMemberView
from . views import DeleteMemberView, CurrentlyIssuedView
from . import views

urlpatterns = [

    # book urls
    path('', views.home, name='home'),
    path('booklist/', BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/new/', AddBookView.as_view(), name='add-book'),
    path('book/<int:pk>/update/', UpdateBookView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', DeleteBookView.as_view(), name='book-delete'),
    path('searchbooks', views.searchBooks, name='search-books'),

    # Member urls
    path('members/', MemberListView.as_view(), name='member-list'),
    path('member/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),
    path('member/new/', AddMemberView.as_view(), name='add-member'),
    path('member/<int:pk>/update/', UpdateMemberView.as_view(), name='member-update'),
    path('member/<int:pk>/delete/', DeleteMemberView.as_view(), name='member-delete'),
    path('searchmember', views.searchMember, name='search-member'),

    # basic library functionalites
    path('member/<int:pk>/issuebook/', views.IssueBook, name='issue-books'),
    path('issuedbooks/', CurrentlyIssuedView.as_view(), name='currently-issued'),
    path('issuedbooks/<int:pk>/returnbook/', views.returnBook, name='return-book'),
    path('returnedbook/', views.TransactionandReturnBook, name='returned-book'),

]
