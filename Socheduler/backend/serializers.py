from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.PostModel
        fields = '__all__'

    def create(self, validated_data: dict):
        user_data = validated_data.pop("user")
        print(user_data)
        user = models.UserModel.objects.create(**user_data)
        user.save()
        new_post = models.PostModel.objects.create(user=user, **validated_data)
        new_post.save()
        return super().create(validated_data)
