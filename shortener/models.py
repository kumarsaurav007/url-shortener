from django.db import models
from django.contrib.auth.models import User

class ShortURL(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="short_urls",
        null=True,
        blank=True
    )
    
    original_url = models.URLField(max_length=2048)

    short_code = models.CharField(
        max_length=10,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.short_code
    
class URLClick(models.Model):
    short_url = models.ForeignKey(
        ShortURL,
        on_delete=models.CASCADE,
        related_name="clicks"
    )
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Click on {self.short_url.short_code} at {self.clicked_at}"