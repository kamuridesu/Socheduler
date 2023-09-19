from typing import Any
from django.db import models

from Socheduler.celery import app


class UserModel(models.Model):
    username = models.CharField(max_length=100, unique=True)
    uuid = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username

    def is_authenticated(self):
        if self.uuid:
            return True
        return False


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(user=None)


class PostModel(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, default=None
    )
    content: str = models.TextField()
    provider = models.CharField(max_length=100)
    token = models.CharField(max_length=255)
    scheduled_date = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    objects = PostManager()


class TaskModel(models.Model):
    task_id = models.CharField(max_length=100, unique=True, blank=False)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs) -> tuple[int, dict[str, int]]:
        app.control.revoke(self.task_id, terminate=True, signal='SIGKILL')
        return super().delete(*args, **kwargs)
