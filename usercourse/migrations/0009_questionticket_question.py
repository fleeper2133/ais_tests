# Generated by Django 4.2.8 on 2024-07-25 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_course_is_demo'),
        ('usercourse', '0008_usercourse_last_visited'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionticket',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.question'),
        ),
    ]
