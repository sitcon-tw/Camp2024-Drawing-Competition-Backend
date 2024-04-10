import logging

from django.contrib.auth.models import User
from django.contrib import auth
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.user import (
    OAuthLoginSerializer,
    UserSerializer,
    UserListSerializer,
    OAuthRegisterSerializer,
)

import secrets
import string


def generate_password(length=12):
    # Define the characters that will be used in the password
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(alphabet) for _ in range(length))
    return password


logger = logging.getLogger(__name__)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="User Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        tags=["account"],
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get("username", "")
        password = data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class Register(APIView):
    @swagger_auto_schema(
        operation_summary="Register",
        operation_description="UserRegister",
        request_body=UserSerializer,
        tags=["account"],
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        user = User.objects.filter(email=email)

        if not user.exists():
            user = User.objects.create_user(username, email, password)
            serializer = UserSerializer(user)
            logger.info(f"User {user.username} register success")
            return Response(
                {"status": "success", "register": True, "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"register": False, "message": "Duplicate Username or Email"},
                status=status.HTTP_409_CONFLICT,
            )


class LogoutAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Logout",
        operation_description="User Logout",
        tags=["account"],
    )
    def get(self, request):
        auth.logout(request)
        return Response(
            {"status": "success", "logout": True}, status=status.HTTP_200_OK
        )


class EditProfileAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Edit Profile",
        operation_description="User Edit Profile",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        tags=["account"],
    )
    def put(self, request):
        username = request.data.get("username", "")
        if username != "":
            user = User.objects.get(username=username)
            if request.data["password"] != "":
                password = request.data["password"]
                user.set_password = password
            if request.data["first_name"] != "":
                first_name = request.data["first_name"]
                user.first_name = first_name
            if request.data["last_name"] != "":
                last_name = request.data["last_name"]
                user.last_name = last_name
            if request.data["email"] != "":
                email = request.data["email"]
                user.email = email
            user.save()
            if user:
                return Response(
                    {"status": "success", "edit": True}, status=status.HTTP_200_OK
                )
        else:
            return Response(
                {"status": "error", "edit": False}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="get users",
        operation_description="get all users",
        tags=["account"],
    )
    def get(self, request, *args, **kwargs):
        query_set = User.objects.all()
        serializer = UserListSerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OAuthUserRegisterAPI(APIView):
    @swagger_auto_schema(
        operation_summary="OAuth User Register",
        operation_description="OAuth User Register",
        request_body=OAuthRegisterSerializer,
        tags=["account"],
    )
    def post(self, request):
        username = request.data.get("username")
        password = generate_password()
        email = request.data.get("email")
        user = User.objects.filter(email=email)

        if not user.exists():
            user = User.objects.create_user(username, email, password)
            serializer = UserSerializer(user)
            logger.info(f"OAuth User {username} Email {email} Joined DataBase")
            return Response(
                {
                    "status": "success",
                    "register": True,
                    "Identity": "OAuth User",
                    "user": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "failed",
                    "register": False,
                    "message": "Duplicate Username or Email",
                },
                status=status.HTTP_409_CONFLICT,
            )


class OAuthUserLoginAPI(APIView):
    @swagger_auto_schema(
        operation_summary="OAuth User Login",
        operation_description="OAuth User Login",
        request_body=OAuthLoginSerializer,
        tags=["account"],
    )
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.get(email=email)
        logger.info(f"OAuth User {user.username} Login")
        serializer = UserSerializer(user)
        return Response(
            {
                "status": "success",
                "login": True,
                "Identity": "OAuth User",
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
