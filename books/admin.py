from django.contrib import admin
from books.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'genre', 'is_published')
    fields = ('title', 'description', 'cover_image', 'genre', 'author', 'is_published', 'price', 'created_at')
    readonly_fields = ('created_at',)


admin.site.register(Book, BookAdmin)
