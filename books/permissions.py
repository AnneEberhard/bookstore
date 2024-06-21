from rest_framework import permissions
import re


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only authors of an object to edit it.

    Assumes the model instance has an 'author' attribute.

    Methods:
        has_object_permission(request, view, obj):
            Check if the request user is the author of the object or if the request method is safe.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the request user is the author of the object or if the request method is safe.

        Args:
            request (HttpRequest): The request object.
            view (View): The view object.
            obj (object): The object instance being accessed.

        Returns:
            bool: True if the request is safe or the user is the author of the object, False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsNotDarthVader(permissions.BasePermission):
    """
    Custom permission to disallow Darth Vader from publishing books.

    Methods:
        has_permission(request, view):
            Check if the request user's username is not 'darthvader'.
    """
    message = "Darth Vader is not allowed to publish books."

    def has_permission(self, request, view):
        """
        Check if the request user's username is not 'darthvader'.

        Args:
            request (HttpRequest): The request object.
            view (View): The view object.

        Returns:
            bool: True if the request user's username is not 'darthvader', False otherwise.
        """
        normalized_username = re.sub(r'[^a-zA-Z]', '', request.user.username).lower()
        return normalized_username != 'darthvader'
