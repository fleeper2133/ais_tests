from celery import shared_task # type: ignore
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser

@shared_task
def delete_expired_demo_users():
    expiration_date = timezone.now() - timedelta(days=3)
    # чекнуть правильность удаления
    CustomUser.objects.filter(username__startswith='demo_test_user', date_joined__lte=expiration_date).delete()
