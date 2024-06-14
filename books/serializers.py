from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Main serializer used when Books are called for from frontend
    """
    cover_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_file_url(self, obj, file_attribute):
        """
        Builds absolute URL to be used in frontend later on.
        Request offers info on how to build the URL.
        """
        file_instance = getattr(obj, file_attribute)
        if file_instance:
            return self.context['request'].build_absolute_uri(file_instance.url)
        return None

    def get_cover_file_url(self, obj):
        """
        Builds an absolute URL for the cover file of the given object.
        """
        return self.get_file_url(obj, 'cover_image')
