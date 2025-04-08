from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        # Automatically assign super admin role based on username or email
        super_admin_usernames = ['admin1', 'admin2', 'admin3']
        super_admin_emails = [
            'mgladney25@basecampcodingacademy.org',
            'afielder25@basecampcodingacademy.org'
        ]

        if instance.username in super_admin_usernames or instance.email in super_admin_emails:
            profile.is_super_admin = True
            profile.save()
