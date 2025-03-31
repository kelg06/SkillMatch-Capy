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
    bio = models.TextField()
    age = models.IntegerField(default=18)
    study_times = models.CharField(max_length=255) 
    classes = models.ManyToManyField(Class)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile_pic.jpg', blank=False, null=False)
    friends = models.ManyToManyField("self", blank=True)


    liked_profiles = models.ManyToManyField("self", symmetrical=False, related_name="liked_by", blank=True)
    disliked_profiles = models.ManyToManyField("self", symmetrical=False, related_name="disliked_by", blank=True)

    def __str__(self):
        return self.user.username

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
