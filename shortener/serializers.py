from rest_framework import serializers

from .models import ShortURL
from django.contrib.auth.models import User
from rest_framework import serializers

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = [
            "id",
            "original_url",
            "short_code",
            "created_at",
            "updated_at",
            "expires_at",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "short_code",
            "created_at",
            "updated_at",
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    password2 = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user