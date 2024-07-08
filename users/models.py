from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from users.managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # добавляем related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # добавляем related_name
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
            CustomUser,
            on_delete=models.CASCADE
            )
    first_name = models.CharField(max_length=150, blank=True, null=True,)
    last_name = models.CharField(max_length=150, blank=True, null=True,)
    surname = models.CharField(max_length=150, blank=True, null=True,)
    # будем использовать для активации пользователя по ссылке из письма с подтверждением
    is_verified = models.BooleanField(default=False)
    img = models.ImageField(blank=True, null=True, upload_to='uploads/')
    phone = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return f"Profile {self.user.email}"

