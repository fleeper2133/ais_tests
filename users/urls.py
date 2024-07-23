# нигде не нашёл пути для пользовательского апи. Поэтому для своих нужд создал и подключил
# к основным путям приложения
from django.urls import path
from .views import CurrentUserAPIView
from .views import CreateDemoUserAPIView

urlpatterns = [
    path('api/current_user/', CurrentUserAPIView.as_view(), name='current_user'),
    path('create_demo_user/', CreateDemoUserAPIView.as_view(), name='create_demo_user'),

]
