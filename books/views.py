from rest_framework import generics
from .permissions import IsAuthorOrReadOnly, IsNotDarthVader
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated


class BookListView(generics.ListAPIView):
    """
    API endpoint that allows listing of books.

    Retrieves a list of all books or filtered by title, genre, or author username.

    Attributes:
        queryset (QuerySet): Queryset of all Book objects.
        serializer_class (BookSerializer): Serializer class for Book model instances.

    Methods:
        get_queryset():
            Retrieves the queryset of books based on query parameters 'title', 'genre', and 'author'.
    """
    queryset = Book.objects.all()
    # queryset =  Book.objects.filter(is_published=True)
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Retrieves the filtered queryset of books based on query parameters.

        Returns:
            QuerySet: Filtered queryset of books.
        """
        queryset = super().get_queryset()
        title = self.request.query_params.get('title')
        genre = self.request.query_params.get('genre')
        author = self.request.query_params.get('author')
        if title:
            queryset = queryset.filter(title__icontains=title)
        if genre:
            queryset = queryset.filter(genre=genre)
        if author:
            queryset = queryset.filter(author__username__icontains=author)
        return queryset


class BookDetailView(generics.RetrieveAPIView):
    """
    API endpoint that allows retrieval of a single book.

    Retrieves details of a specific book identified by its primary key.

    Attributes:
        queryset (QuerySet): Queryset of all Book objects.
        serializer_class (BookSerializer): Serializer class for Book model instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(generics.CreateAPIView):
    """
    API endpoint that allows creation of a new book.

    Creates a new book instance with the current authenticated user as the author.

    Attributes:
        queryset (QuerySet): Queryset of all Book objects.
        serializer_class (BookSerializer): Serializer class for Book model instances.
        permission_classes (list): List of permission classes, requires authentication and excludes 'darthvader'.

    Methods:
        perform_create(serializer):
            Saves the newly created book with the current authenticated user as the author.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsNotDarthVader]

    def perform_create(self, serializer):
        """
        Saves the newly created book with the current authenticated user as the author.

        Args:
            serializer (BookSerializer): Serializer instance containing validated data for the new book.
        """
        serializer.save(author=self.request.user)


class BookUpdateView(generics.UpdateAPIView):
    """
    API endpoint that allows updating an existing book.

    Updates details of a specific book identified by its primary key.
    Only the author of the book can update it.

    Attributes:
        queryset (QuerySet): Queryset of all Book objects.
        serializer_class (BookSerializer): Serializer class for Book model instances.
        permission_classes (list): List of permission classes, requires authentication and author-only access.

    Methods:
        perform_update(serializer):
            Saves the updated details of the book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        """
        Saves the updated details of the book.

        Args:
            serializer (BookSerializer): Serializer instance containing validated data for updating the book.
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    API endpoint that allows deletion of an existing book.

    Deletes a specific book identified by its primary key.
    Only the author of the book can delete it.

    Attributes:
        queryset (QuerySet): Queryset of all Book objects.
        serializer_class (BookSerializer): Serializer class for Book model instances.
        permission_classes (list): List of permission classes, requires authentication and author-only access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
