# Generated by Django 5.1.2 on 2025-03-27 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics/'),
        ),
    ]
