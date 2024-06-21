from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.

    Serializes CustomUser objects into JSON representations and vice versa.

    Attributes:
        model (CustomUser): CustomUser model class.
        fields (list): List of fields to be serialized.

    Meta:
        model (CustomUser): Specifies the model class to be serialized.
        fields (list): List of fields from CustomUser model to include in serialization.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'author_pseudonym']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Serializes user registration data and validates password encryption.

    Attributes:
        password (CharField): Write-only field for user password.
        model (CustomUser): CustomUser model class.
        fields (list): List of fields to be serialized.

    Meta:
        model (CustomUser): Specifies the model class to be serialized.
        fields (list): List of fields from CustomUser model to include in serialization, including password.

    Methods:
        create(validated_data):
            Creates a new user with encrypted password from validated data.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'author_pseudonym', 'password']

    def create(self, validated_data):
        """
        Creates a new user with encrypted password from validated data.

        Args:
            validated_data (dict): Dictionary containing validated user registration data.

        Returns:
            CustomUser: Newly created user instance.
        """
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
