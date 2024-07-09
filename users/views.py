from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from users.models import CustomUser as User
from users.serializers import UserSerializer, RegistrationSerializer
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiRequest,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.core.mail import EmailMessage
from rest_framework import permissions


class SendMail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=inline_serializer(
            name="user",
            fields={
                "email": serializers.EmailField(),
                "title": serializers.CharField(),
                "description": serializers.CharField(),
            },
        )
    )
    def post(self, request):
        data = request.data
        email = data.get("email")
        title = data.get("title")
        description = data.get("description")
        if not email:
            email_send = EmailMessage(title, description, to=[request.user.email])
        else:
            email_send = EmailMessage(title, description, to=[email])
        email_send.send()

        return Response(
            {
                "success": True
            },
            status=status.HTTP_200_OK,
        )


class LoginAPIView(APIView):
    @extend_schema(
        request=inline_serializer(
            name="user",
            fields={
                "email": serializers.EmailField(),
                "password": serializers.CharField(),
            },
        )
    )
    def post(self, request):
        data = request.data
        email = data.get("email", None)
        password = data.get("password", None)
        if email is None or password is None:
            return Response(
                {"error": "Нужен и логин, и пароль"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(email=email, password=password)
        login(request, user)
        # __import__('ipdb').set_trace()

        if user is None:
            return Response(
                {"error": "Неверные данные"}, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({"user_id": user.id, "email": user.email})

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class RegistrationAPIView(APIView):
    @extend_schema(
        request=inline_serializer(
            name="registration",
            fields={
                "email": serializers.EmailField(),
                "password": serializers.CharField(),
                "password_confirm": serializers.CharField(),
            },
        )
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user is not None:
                refresh = RefreshToken.for_user(user)  # Создание Refesh и Access
                refresh.payload.update(
                    {  # Полезная информация в самом токене
                        "user_id": user.id,
                        "email": user.email,
                    }
                )

                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),  # Отправка на клиент
                    },
                    status=status.HTTP_201_CREATED,
                )

        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutAPIView(APIView):
    @extend_schema(
        request=inline_serializer(
            name="logout",
            fields={
                "refresh_token": serializers.CharField(),
            },
        )
    )
    def post(self, request):
        logout(request)
        refresh_token = request.data.get(
            "refresh_token"
        )  # С клиента нужно отправить refresh token
        if not refresh_token:
            return Response(
                {"error": "Необходим Refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавить его в чёрный список

        except Exception as e:
            return Response(
                {"error": "Неверный Refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"success": "Выход успешен"}, status=status.HTTP_200_OK)
