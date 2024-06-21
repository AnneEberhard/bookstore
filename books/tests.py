from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from .models import Book
from .serializers import BookSerializer


class BookListViewTests(APITestCase):

    def setUp(self):
        self.author1 = CustomUser.objects.create_user(username='author1', password='password')
        self.author2 = CustomUser.objects.create_user(username='author2', password='password')

        self.book1 = Book.objects.create(title='Book 1', genre='Fiction', author=self.author1)
        self.book2 = Book.objects.create(title='Book 2', genre='Fantasy', author=self.author2)
        self.book3 = Book.objects.create(title='Book 3', genre='Fiction', author=self.author1)

    def test_filter_by_title(self):
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'Book 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = BookSerializer([self.book1], many=True).data
        self.assertEqual(response.data, serializer_data)

    def test_filter_by_genre(self):
        url = reverse('book-list')
        response = self.client.get(url, {'genre': 'Fiction'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = BookSerializer([self.book1, self.book3], many=True).data
        self.assertEqual(response.data, serializer_data)

    def test_filter_by_author(self):
        url = reverse('book-list')
        response = self.client.get(url, {'author': 'author1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = BookSerializer([self.book1, self.book3], many=True).data
        self.assertEqual(response.data, serializer_data)

    def test_filter_by_multiple_parameters(self):
        url = reverse('book-list')
        response = self.client.get(url, {'genre': 'Fiction', 'author': 'author1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = BookSerializer([self.book1, self.book3], many=True).data
        self.assertEqual(response.data, serializer_data)

    def test_no_filter_parameters(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = BookSerializer([self.book1, self.book2, self.book3], many=True).data
        self.assertEqual(response.data, serializer_data)


class BookViewsTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password123')
        self.user2 = CustomUser.objects.create_user(username='testuser2', password='password')
        self.book = Book.objects.create(
            title='Test Book',
            genre='Fantasy',
            author=self.user
        )

    def test_book_detail_view(self):
        url = reverse('book-detail', args=[self.book.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer_data = BookSerializer(self.book).data
        self.assertEqual(response.data, serializer_data)

    def test_book_create_view(self):
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'genre': 'Fantasy',
            'description': 'Description',
            'author': self.user,
            'is_published': True,
            'price': 0
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Überprüfe, ob das Buch tatsächlich erstellt wurde
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_book_update_view(self):
        url = reverse('book-edit', args=[self.book.pk])
        data = {
            'title': 'Updated Book',
            'genre': 'Fantasy',
            'description': 'Description',
            'is_published': True,
            'price': 0
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_book_update_wrong_author_view(self):
        url = reverse('book-edit', args=[self.book.pk])
        data = {
            'title': 'Updated Book',
            'genre': 'Fantasy',
            'description': 'Description',
            'is_published': True,
            'price': 0
        }
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_delete_view(self):
        url = reverse('book-delete', args=[self.book.pk])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_book_delete_wrong_author_view(self):
        url = reverse('book-delete', args=[self.book.pk])
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())
