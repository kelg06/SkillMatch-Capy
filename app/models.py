from django.contrib.auth.models import User
from django.db import models

# List of Ole Miss classes
OLE_MISS_CLASSES = [
    ("CSCI 111", "CSCI 111 - Computer Science I"),
    ("CSCI 112", "CSCI 112 - Computer Science II"),
    ("MATH 261", "MATH 261 - Calculus I"),
    ("MATH 262", "MATH 262 - Calculus II"),
    # Add more classes here...
]

class Class(models.Model):
    name = models.CharField(max_length=100, choices=OLE_MISS_CLASSES, unique=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
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
    
    # Study times (Dropdown of predefined times, required)
    STUDY_TIME_CHOICES = [
        ('1 AM', '1 AM'),
        ('2 AM', '2 AM'),
        ('3 AM', '3 AM'),
        ('4 AM', '4 AM'),
        ('5 AM', '5 AM'),
        ('6 AM', '6 AM'),
        ('7 AM', '7 AM'),
        ('8 AM', '8 AM'),
        ('9 AM', '9 AM'),
        ('10 AM', '10 AM'),
        ('11 AM', '11 AM'),
        ('12 PM', '12 PM'),
        ('1 PM', '1 PM'),
        ('2 PM', '2 PM'),
        ('3 PM', '3 PM'),
        ('4 PM', '4 PM'),
        ('5 PM', '5 PM'),
        ('6 PM', '6 PM'),
        ('7 PM', '7 PM'),
        ('8 PM', '8 PM'),
        ('9 PM', '9 PM'),
        ('10 PM', '10 PM'),
        ('11 PM', '11 PM'),
        ('12 AM', '12 AM')
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
    friends = models.ManyToManyField("self", blank=True)
    
    # Liked and disliked profiles for swipe functionality
    liked_profiles = models.ManyToManyField("self", symmetrical=False, related_name="liked_by", blank=True)
    disliked_profiles = models.ManyToManyField("self", symmetrical=False, related_name="disliked_by", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')
        
    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({'Accepted' if self.accepted else 'Pending'})"

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
