from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone
from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        read_only_fields = ("id",)


class OAuthRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class OAuthLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
