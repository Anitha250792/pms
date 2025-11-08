from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds 'role' and 'department' fields for role-based access
    (Manager, Team Member, Design Team, HR) and a flag to know
    whether the user has already chosen their role.
    """

    ROLE_MANAGER = "Manager"
    ROLE_MEMBER = "Team Member"
    ROLE_DESIGN = "Design Team"
    ROLE_HR = "HR"

    ROLE_CHOICES = [
        (ROLE_MANAGER, "Manager"),
        (ROLE_MEMBER, "Team Member"),
        (ROLE_DESIGN, "Design Team"),
        (ROLE_HR, "HR"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER,
        verbose_name="User Role",
        blank=True,
        null=True,
    )

    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Department",
    )

    # ✅ New: used to show the “Choose your role” prompt only once
    is_role_selected = models.BooleanField(
        default=False,
        verbose_name="Has selected role"
    )

    def __str__(self):
        return f"{self.username} ({self.role or 'No role'})"
