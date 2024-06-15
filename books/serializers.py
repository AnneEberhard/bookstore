from rest_framework import serializers

from users.serializers import CustomUserSerializer
from .models import Book
from users.models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    """
    Main serializer used when Books are called for from frontend
    """
    cover_image = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

    def get_cover_image(self, obj):
        """
        Builds an absolute URL for the cover file of the given object.
        """
        request = self.context.get('request')
        if obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url)
        return None
