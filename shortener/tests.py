from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.cache import cache

from django.utils import timezone
from datetime import timedelta

from .tasks import deactivate_expired_urls

from .models import ShortURL, URLClick

class ShortURLModelTest(TestCase):

    def test_short_url_can_be_created(self):
        short_url = ShortURL.objects.create(
            original_url="https://www.google.com",
            short_code="test123",
        )

        self.assertEqual(
            short_url.original_url,
            "https://www.google.com"
        )

        self.assertEqual(
            short_url.short_code,
            "test123"
        )

class ShortURLCreateAPITest(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_create_short_url(self):
        response = self.client.post(
            "/api/urls/",
            {
                "original_url": "https://www.google.com"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            ShortURL.objects.count(),
            1
        )

    def test_create_short_url_requires_authentication(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            "/api/urls/",
            {
                "original_url": "https://www.google.com"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

class ShortURLRedirectTest(APITestCase):

    def setUp(self):
        cache.clear()

        User = get_user_model()

        self.user = User.objects.create_user(
            username="redirectuser",
            password="testpassword123"
        )

        self.short_url = ShortURL.objects.create(
            user=self.user,
            original_url="https://www.google.com",
            short_code="redir123",
        )

    def test_short_url_redirects(self):
        response = self.client.get(
            "/api/redir123/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND
        )

        self.assertEqual(
            response.url,
            "https://www.google.com"
        )

    def test_redirect_creates_click_record(self):
        response = self.client.get(
            "/api/redir123/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND
        )

        self.assertEqual(
            URLClick.objects.filter(
                short_url=self.short_url
            ).count(),
            1
        )

class ShortURLAnalyticsTest(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="analyticsuser",
            password="testpassword123"
        )

        self.short_url = ShortURL.objects.create(
            user=self.user,
            original_url="https://www.google.com",
            short_code="analytics",
        )

        URLClick.objects.create(
            short_url=self.short_url,
            ip_address="127.0.0.1",
            user_agent="Test Browser",
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_analytics_returns_clicks(self):
        response = self.client.get(
            f"/api/urls/{self.short_url.id}/analytics/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

class CeleryTaskTest(TestCase):

    def test_deactivate_expired_urls(self):
        user = get_user_model().objects.create_user(
            username="celeryuser",
            password="testpassword123"
        )

        short_url = ShortURL.objects.create(
            user=user,
            original_url="https://www.google.com",
            short_code="celery123",
            is_active=True,
            expires_at=timezone.now() - timedelta(minutes=10),
        )

        result = deactivate_expired_urls()

        short_url.refresh_from_db()

        self.assertFalse(short_url.is_active)

        self.assertEqual(
            result,
            "1 URLs deactivated."
        )