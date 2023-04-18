# Generated by Django 4.2 on 2023-04-17 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0002_hashtag_image_post_socialmediaaccount_video_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="socialmediaaccount",
            name="platform",
            field=models.CharField(
                choices=[
                    ("FB", "Facebook"),
                    ("TW", "Twitter"),
                    ("IG", "Instagram"),
                    ("LI", "LinkedIn"),
                ],
                max_length=2,
            ),
        ),
    ]
