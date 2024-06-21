from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'author_pseudonym')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('author_pseudonym',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
