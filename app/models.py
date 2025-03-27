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
    bio = models.TextField(blank=True)
    age = models.IntegerField(null=True, blank=True)
    study_times = models.CharField(max_length=255, blank=True)  # Example: "Morning, Afternoon"
    classes = models.ManyToManyField(Class, blank=True)  # Many-to-Many relationship
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile_pic.jpg', blank=False, null=False)

    # Swiping functionality
    liked_profiles = models.ManyToManyField("self", symmetrical=False, related_name="liked_by", blank=True)
    disliked_profiles = models.ManyToManyField("self", symmetrical=False, related_name="disliked_by", blank=True)

    def __str__(self):
        return self.user.username
