from datetime import date
from django.db import models
from users.models import CustomUser


class Book(models.Model):
    """
    Model representing a book in the bookstore.

    Attributes:
        created_at (DateField): The date when the book was created.
        title (CharField): The title of the book.
        url_title (CharField): The URL-friendly version of the book title.
        description (CharField): A brief description of the book.
        cover_image (FileField): The image file of the book's cover.
        genre (CharField): The genre of the book chosen from predefined choices.
        author (ForeignKey): The author of the book, linked to a CustomUser instance.
        is_published (BooleanField): Indicates if the book is published or not.
        price (DecimalField): The price of the book.

    Methods:
        __str__(): Returns the string representation of the book instance.
        save(): Overrides the save method to generate a URL-friendly title if not provided.

    """
    GENRE_CHOICES = [
        ('Dystopia', 'Dystopia'),
        ('Fantasy', 'Fantasy'),
        ('Historical', 'Historical'),
        ('Spy', 'Spy'),
        ('Contemporary', 'Contemporary'),
        ('Unclassified', 'Unclassified'),
    ]

    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=80)
    url_title = models.CharField(max_length=80, default='', blank=True, null=True)
    description = models.CharField(max_length=1500)
    cover_image = models.FileField(upload_to='covers', blank=True, null=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10)

    def __str__(self):
        """
        Returns the string representation of the book instance.

        Returns:
            str: The title of the book.
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a URL-friendly title if not provided.
        """
        if not self.url_title:
            self.url_title = self.generate_url_title()
        super().save(*args, **kwargs)

    def generate_url_title(self):
        """
        Generates a URL-friendly version of the book title.

        Returns:
            str: The URL-friendly title.
        """
        return self.title.replace(' ', '_')
