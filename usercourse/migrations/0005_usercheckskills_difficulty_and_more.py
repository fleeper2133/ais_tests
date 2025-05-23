# Generated by Django 4.2.8 on 2024-07-22 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usercourse', '0004_alter_questionticket_user_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercheckskills',
            name='difficulty',
            field=models.CharField(blank=True, choices=[('Easy', 'Легко'), ('Medium', 'Средне'), ('Hard', 'Сложно'), ('Extrem', 'Невозможно')], default='Medium', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='usercheckskills',
            name='user_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usercourse.usercourse'),
        ),
    ]
