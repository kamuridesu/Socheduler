from rest_framework import serializers

from . import models


class SocialAccontSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SocialMediaAccount
        fields = ["id", "username", "platform"]

    def create(self, validated_data):
        return super().create(validated_data)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ["id", "image_file"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = ["id", "video_file"]


class PostSerializer(serializers.ModelSerializer):
    account_username = serializers.CharField(max_length=100, write_only=True)
    images = ImageSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = ["id", "account_username", "content", "scheduled_datetime", "is_published", "images", "videos"]

    def create(self, validated_data: dict):
        username: dict = validated_data.pop("account_username")
        try:
            user_account = models.SocialMediaAccount.objects.get(username=username)
        except models.SocialMediaAccount.DoesNotExist:
            raise serializers.ValidationError(f"Social media account with username '{username}' does not exist.")
        new_post = models.Post(account=user_account, **validated_data)
        new_post.save()
        return new_post
