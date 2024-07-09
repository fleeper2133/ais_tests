from rest_framework import serializers
from users.models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    # Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    # и так же что он не может быть прочитан клиентской стороной
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    password_confirm = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ('email', 'password', 'password_confirm', 'token')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают!"})

        return attrs

    def create(self, validated_data):
        if "password_confirm" in validated_data:
            validated_data.pop('password_confirm')
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return CustomUser.objects.create_user(**validated_data)

# Сериализатор для модели User
# Он использует все поля модели User
# больше не требуется, надо убрать
#TODO: fix this
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"