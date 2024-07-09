from users.views import LoginAPIView, LogoutAPIView, RegistrationAPIView, SendMail
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send-mail/', SendMail.as_view(), name="send_mail")
]