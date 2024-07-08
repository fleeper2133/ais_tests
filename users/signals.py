from users.models import CustomUser, Profile

from django.db.models.signals import post_save
from django.dispatch import receiver


# Создаем по сигналу post_save Profile
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Сохраняем по сигналу Profile после сохранения CustomUser
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
