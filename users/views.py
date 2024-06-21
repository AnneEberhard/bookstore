from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .models import CustomUser


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.

    Allows creation of a new user with provided user data.

    Attributes:
        queryset (QuerySet): Queryset of all CustomUser objects.
        serializer_class (RegisterSerializer): Serializer class for user registration data.

    Methods:
        create(request, *args, **kwargs):
            Handles POST requests to create a new user.
            Returns a response with the serialized user data and a success message upon successful registration.
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new user.

        Args:
            request (Request): HTTP request object containing user registration data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response containing the serialized user data and a success message.

        Raises:
            ValidationError: If the serializer validation fails.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": RegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)
