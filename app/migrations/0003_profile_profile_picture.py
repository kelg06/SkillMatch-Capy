# Generated by Django 5.1.2 on 2025-03-27 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_profile_disliked_profiles_profile_liked_profiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
