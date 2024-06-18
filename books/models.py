from datetime import date
from django.db import models

from users.models import CustomUser


class Book(models.Model):
    """
    The main model for books
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

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.url_title:
            self.url_title = self.generate_url_title()
        super().save(*args, **kwargs)
        if self.cover_image:
            print("Cover image path:", self.cover_image.path)
        else:
            print("No cover image")

    def generate_url_title(self):
        return self.title.replace(' ', '_')
