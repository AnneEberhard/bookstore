from rest_framework import permissions
import re

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsNotDarthVader(permissions.BasePermission):
    message = "Darth Vader is not allowed to publish books."

    def has_permission(self, request, view):
        normalized_username = re.sub(r'[^a-zA-Z]', '', request.user.username).lower()
        return normalized_username != 'darthvader'
