from django.urls import path

from .views import RegisterView, ShortURLCreateView, ShortURLDetailView, ShortURLRedirectView, ShortURLAnalyticsView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    path("urls/", ShortURLCreateView.as_view(), name="create-short-url"),
    path("<str:short_code>/", ShortURLRedirectView.as_view(), name="redirect-short-url"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("urls/<int:pk>/", ShortURLDetailView.as_view(), name="short-url-detail"),
    path("urls/<int:pk>/analytics/", ShortURLAnalyticsView.as_view(), name="short-url-analytics"),
]