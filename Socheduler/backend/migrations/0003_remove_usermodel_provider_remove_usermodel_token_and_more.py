# Generated by Django 4.2 on 2023-04-25 19:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0002_usermodel_uuid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usermodel",
            name="provider",
        ),
        migrations.RemoveField(
            model_name="usermodel",
            name="token",
        ),
        migrations.AddField(
            model_name="postmodel",
            name="provider",
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="postmodel",
            name="token",
            field=models.CharField(default=None, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]