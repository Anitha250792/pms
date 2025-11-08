from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for CustomUser model.
    Keeps all default UserAdmin features, adds Role field for display, filtering, and editing.
    """

    # Columns visible in the user list
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

    # Filters in the right sidebar
    list_filter = ('role', 'is_staff', 'is_active')

    # Add 'role' to the existing fieldsets (for editing existing users)
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role', 'department')}),
    )

    # Add 'role' and 'department' to the "Add User" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role', 'department')}),
    )
