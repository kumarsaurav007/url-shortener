from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, ShortURLSerializer
from .services import generate_short_code
from django.shortcuts import get_object_or_404, redirect
from .models import ShortURL, URLClick
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from django.core.cache import cache


class ShortURLCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        short_urls = ShortURL.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = ShortURLSerializer(
            short_urls,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ShortURLSerializer(data=request.data)

        if serializer.is_valid():
            short_code = generate_short_code()

            short_url = serializer.save(
                short_code=short_code,
                user=request.user
            )

            response_serializer = ShortURLSerializer(short_url)

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ShortURLRedirectView(APIView):

    def get(self, request, short_code):
        cache_key = f"short_url:{short_code}"

        cached_url = cache.get(cache_key)

        if cached_url:
            original_url = cached_url
            short_url = get_object_or_404(
                ShortURL,
                short_code=short_code
            )
        else:
            short_url = get_object_or_404(
                ShortURL,
                short_code=short_code,
                is_active=True
            )

            if short_url.expires_at and short_url.expires_at <= timezone.now():
                return Response(
                    {"detail": "This short URL has expired."},
                    status=status.HTTP_410_GONE
                )

            original_url = short_url.original_url

            cache.set(
                cache_key,
                original_url,
                timeout=60 * 15
            )

        URLClick.objects.create(
            short_url=short_url,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT")
        )

        return redirect(original_url)
    
    def get_client_ip(self, request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

        if forwarded:
            return forwarded.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR")
    
class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "message": "User registered successfully.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ShortURLDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            short_url = ShortURL.objects.get(
                id=pk,
                user=request.user
            )
        except ShortURL.DoesNotExist:
            return Response(
                {"error": "URL not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ShortURLSerializer(short_url)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        try:
            short_url = ShortURL.objects.get(
                id=pk,
                user=request.user
            )
        except ShortURL.DoesNotExist:
            return Response(
                {"error": "URL not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ShortURLSerializer(
            short_url,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            cache.delete(
                f"short_url:{short_url.short_code}"
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        try:
            short_url = ShortURL.objects.get(
                id=pk,
                user=request.user
            )
        except ShortURL.DoesNotExist:
            return Response(
                {"error": "URL not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        cache.delete(
            f"short_url:{short_url.short_code}"
        )

        short_url.delete()

        return Response(
            {"message": "URL deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
    
class ShortURLAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            short_url = ShortURL.objects.get(
                id=pk,
                user=request.user
            )
        except ShortURL.DoesNotExist:
            return Response(
                {"error": "URL not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        clicks = short_url.clicks.order_by("-clicked_at")

        data = {
            "short_code": short_url.short_code,
            "original_url": short_url.original_url,
            "total_clicks": clicks.count(),
            "clicks": [
                {
                    "clicked_at": click.clicked_at,
                    "ip_address": click.ip_address,
                    "user_agent": click.user_agent,
                }
                for click in clicks
            ]
        }

        return Response(
            data,
            status=status.HTTP_200_OK
        )