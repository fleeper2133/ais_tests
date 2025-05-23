# Generated by Django 4.2.8 on 2024-07-15 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usercourse', '0002_alter_taskquestion_user_alter_useranswer_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercourse',
            name='selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usercourse',
            name='status',
            field=models.CharField(blank=True, choices=[('New', 'Новый'), ('In progress', 'В процессе'), ('Completed', 'Пройденный'), ('Delayed', 'Отложенный')], default='New', max_length=255, null=True),
        ),
    ]
