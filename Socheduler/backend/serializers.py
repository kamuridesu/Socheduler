from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, write_only=True)
    token = serializers.CharField(max_length=255, write_only=True)
    provider = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = models.PostModel
        fields = '__all__'

    def create(self, validated_data: dict):
        user, created = models.UserModel.objects.get_or_create(username=validated_data.pop("username"), token=validated_data.pop("token"), provider=validated_data.pop("provider"))
        if created:
            user.save()
        print(user)
        print("valiodated data: ")
        print(validated_data)
        new_post = models.PostModel.objects.create(user=user, **validated_data)
        new_post.save()
        return new_post
