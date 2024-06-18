from django.urls import path
from .views import BookCreateView, BookDeleteView, BookUpdateView, BookListView, BookDetailView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('edit/<int:pk>/', BookUpdateView.as_view(), name='book-edit'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]
