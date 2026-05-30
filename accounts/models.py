from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Stores extra profile details for each customer."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=24, blank=True)
    city = models.CharField(max_length=80, blank=True)
    favorite_collection = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
