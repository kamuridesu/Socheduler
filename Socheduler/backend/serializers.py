from rest_framework import serializers

from . import models
from .tasks import createGist
from datetime import datetime, timezone
from celery.result import AsyncResult


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ["username", "uuid", "provider"]


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, write_only=True)
    uuid = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = models.PostModel
        fields = "__all__"

    def create(self, validated_data: dict):
        user, created = models.UserModel.objects.get_or_create(
            username=validated_data.pop("username"), uuid=validated_data.pop("uuid")
        )
        if created:
            user.save()

        new_post = models.PostModel.objects.create(user=user, **validated_data)
        new_post.save()

        countdown = (new_post.scheduled_date - datetime.now(timezone.utc)).total_seconds()
        task: AsyncResult = createGist.apply_async(args=(new_post.pk, new_post.token, new_post.content), countdown=round(countdown))
        new_task = models.TaskModel.objects.create(task_id=task.id, post=new_post)
        new_task.save()

        return new_post
