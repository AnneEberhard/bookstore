from django.urls import path
from .views import BookCreateView, BookDeleteView, BookUpdateView, BookListView, BookDetailView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name='book-edit'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
