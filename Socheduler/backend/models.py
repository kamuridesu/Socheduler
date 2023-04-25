from django.db import models


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
