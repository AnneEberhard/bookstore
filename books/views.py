from rest_framework import generics
from .permissions import IsAuthorOrReadOnly, IsNotDarthVader
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    # queryset =  Book.objects.filter(is_published=True)
    serializer_class = BookSerializer

    def get_queryset(self):
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
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsNotDarthVader]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
