from django.db import models



PLATFORMS = [
    ("FB", "Facebook"),
    ("TW", "Twitter"),
    ("IG", "Instagram"),
    ("LI", "LinkedIn"),
]


class SocialMediaAccount(models.Model):
    username = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} ({self.platform})"

    def __repr__(self):
        return f"SocialMediaAccount(username='{self.username}', platform='{self.platform}')"


class Post(models.Model):
    account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)
    content = models.TextField()
    scheduled_datetime = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"Post #{self.pk} ({self.account})"

    def __repr__(self):
        return f"Post(account={self.account}, content='{self.content}', scheduled_datetime='{self.scheduled_datetime}', is_published='{self.is_published}')"


class Hashtag(models.Model):
    name = models.CharField(max_length=100)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Hashtag(name='{self.name}')"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to="media")

    def __str__(self):
        return f"Image #{self.pk} (post #{self.post.pk})"

    def __repr__(self):
        return f"Image(post={self.post}, image_file='{self.image_file.name}')"


class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to="media")

    def __str__(self):
        return f"Video #{self.pk} (post #{self.post.pk})"

    def __repr__(self):
        return f"Video(post={self.post}, video_file='{self.video_file.name}')"
