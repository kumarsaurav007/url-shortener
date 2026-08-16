from celery import shared_task
from django.utils import timezone

from .models import ShortURL

@shared_task
def deactivate_expired_urls():
    expired_urls = ShortURL.objects.filter(
        expires_at__isnull=False,
        expires_at__lte=timezone.now(),
        is_active=True,
    )

    count = expired_urls.update(is_active=False)

    return f"{count} URLs deactivated."