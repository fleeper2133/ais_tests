# Generated by Django 4.2.8 on 2024-07-15 14:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0002_alter_qualification_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="name",
            field=models.TextField(db_index=True),
        ),
    ]
