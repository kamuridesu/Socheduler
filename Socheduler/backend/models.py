from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, token, provider):
        user = self.model(username=username, token=token, provider=provider)
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    token = models.CharField(max_length=255, unique=True)
    provider = models.CharField(max_length=100)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['token', 'provider']

    def __str__(self):
        return self.username

    def is_authenticated(self):
        return True


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(user=None)

class PostModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, default=None)
    content: str = models.TextField()
    scheduled_date = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    objects = PostManager()