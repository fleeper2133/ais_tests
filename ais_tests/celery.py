from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ais_tests.settings')
app = Celery('ais_tests')

# Используем строку здесь, чтобы работник не должен был сериализовать объект конфигурации.
# - namespace='CELERY' означает, что все настройки Celery должны иметь префикс `CELERY_`.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Настройка периодической задачи для удаления демо-пользователей
app.conf.beat_schedule = {
    'delete-expired-demo-users': {
        'task': 'users.tasks.delete_expired_demo_users',
        'schedule': crontab(hour=0, minute=0),  # Запуск каждый день
    },
}

# пропущена настройка файла __init__.py
# Команды для запуска celery
# redis-server
# celery -A your_project_name worker -l info
# celery -A your_project_name beat -l info
