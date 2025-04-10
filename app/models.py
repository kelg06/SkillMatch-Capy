from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Admin roles
    is_super_admin = models.BooleanField(default=False)
    is_group_admin = models.BooleanField(default=False)
    
    # First and last name (Required)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    
    # Age (Required)
    age = models.IntegerField(default=18, null=False, blank=False)
    
    # Hometown (Required)
    hometown = models.CharField(max_length=100, null=False, blank=False)
    
    # Major and Minor (Required)
    major = models.CharField(max_length=100, null=False, blank=False)
    minor = models.CharField(max_length=100, blank=True, null=True)
    
    # Grade (Required)
    grade = models.CharField(max_length=20, null=False, blank=False)
    
    # Gender (Required)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=False, blank=False)
    
    # Preferred Gender (Optional)
    preferred_gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    
    # Study times (Dropdown of predefined times, required)
    STUDY_TIME_CHOICES = [
        # ... existing choices ...
    ]
    
    study_times = models.CharField(
        max_length=20,
        choices=STUDY_TIME_CHOICES,
        null=False, 
        blank=False
    )

    # Additional fields
    hobbies = models.TextField(blank=True, null=True)
    clubs_and_extracurriculars = models.TextField(blank=True, null=True)
    goals_after = models.CharField(max_length=255, null=False, blank=False)

    # Profile Picture (Required)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile_pic.jpg', blank=False, null=False)
    
    # Many-to-many relationships
    friends = models.ManyToManyField("self", blank=True)  # For confirmed friends
    pending_sent_requests = models.ManyToManyField("self", symmetrical=False, related_name="pending_received_requests", blank=True)
    liked_profiles = models.ManyToManyField("self", symmetrical=False, related_name="liked_by", blank=True)
    disliked_profiles = models.ManyToManyField("self", symmetrical=False, related_name="disliked_by", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)  # Added declined field
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username} - {'Accepted' if self.accepted else 'Pending'}"

class Chat(models.Model):
    user1 = models.ForeignKey(User, related_name='chat_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chat_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"

    @property
    def participants(self):
        return [self.user1, self.user2]


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username}: {self.content[:30]}..."

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    days = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    

# FLYER AREA---
class GroupPost(models.Model):
    title = models.CharField(max_length=200,blank=True)
    image = models.ImageField(upload_to='group_flyers/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
