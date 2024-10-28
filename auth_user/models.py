from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True, editable=True)
    date_of_birth = models.DateField(null=True)
    user_gender = models.CharField(
        max_length=10,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ],
        null=True,
    )
    position_status = models.CharField(
        max_length=20,
        choices=[
            ("Student", "Student"),
            ("Admin", "Admin"),
            ("Faculty", "Faculty"),
        ],
        null=True,
    )

    # Add related_name attributes to prevent clashes with default auth.User groups and permissions
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  # Change related_name to prevent clash with auth.User.groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  # Change related_name to prevent clash with auth.User.user_permissions
        blank=True,
    )

    def __str__(self):
        return self.username
