from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_match_index = models.IntegerField(default=0)
    last_seen = models.DateTimeField(null=True, blank=True)


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

    GENDER_CHOICES_1 = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]

    GENDER_CHOICES_2 = [
        ('', 'Either'),
        ('male', 'Male'),
        ('female', 'Female')
    ]

    CAMPUS_GROUP_CHOICES=[
        ('fraternity_sorority', '🏛 Fraternity/Sorority'), ('academic_clubs', '🧠 Academic clubs (e.g., Honors College, debate, CME)'), 
        ('creative_orgs', '🎨 Creative orgs (e.g., theatre, film, writing)'), 
        ('sports_intramurals', '🎽 Sports or intramurals'), 
        ('music_arts_groups', '🎸 Music or arts-related groups'),
        ('religious_orgs', '🙏 Religious orgs (e.g., Cru, Young Life, RUF)'), ('service_groups', '🌍 Service & volunteer groups'), 
        ('niche_clubs', '🧩 Niche interest clubs (e.g., gaming, outdoors, crypto, chess)'), 
        ('not_involved', '🚫 Not involved (yet!)')]

    GHOST_LIKELIHOOD_CHOICES = [(str(i), str(i)) for i in range(0, 11)]

    # Questionnaire beginning
    # -----------------------
    # Questionnaire beginning
    grove_or_game_day = models.CharField(max_length=50, choices=[('grove', '📚 The Grove on a quiet day'), ('game_day', '🐅 Game day in the student section')])
    ideal_study_spot = models.CharField(max_length=50, choices=[('ajax', '🍳 Diner booth'), ('library', '📖 Library'), ('uptown', '☕ Coffee Shop'), ('couch', '🏡 At Home')])
    study_time = models.CharField(max_length=50, choices=[('morning', '🌅 Morning'), ('afternoon', '🌞 Afternoon'), ('late_night', '🌙 Late night')])
    energy_source = models.CharField(max_length=50, choices=[('music', '🎧 Music'), ('walks', '🚶 Walks around campus'), ('caffeine', '☕ Caffeine'), ('friends', '👯 Friends')])
    group_project_role = models.CharField(max_length=50, choices=[('lead', '✅ Take the lead'), ('quiet', '✍️ Do the work quietly'), ('organizer', '👥 Organize the group'), ('panic', '😅 Panic last minute (but pull through)')])
    exam_prep_style = models.CharField(max_length=50, choices=[('solo', 'Solo cram session'), ('flashcards', 'Flashcards and repetition'), ('group', 'Group review'), ('teach', 'Teaching someone else')])
    academic_strength = models.CharField(max_length=50, choices=[('detail', '🔍 Focused & detail-oriented'), ('creative', '💭 Creative problem-solver'), ('fast', '🧠 Fast learner'), ('communicator', '💬 Good communicator')])
    accountability_style = models.CharField(max_length=50, choices=[('daily', 'Daily check-ins'), ('deadlines', 'Deadlines & reminders'), ('casual', 'Casual “you good?” texts'), ('self', 'None—I’m self-driven (usually)')])
    wish_more_of = models.CharField(max_length=50, choices=[('time', '⏳ Time'), ('money', '💰 Money'), ('focus', '🧠 Focus'), ('study_buddies', '🙌 Chill people to study with')])
    hot_take = models.CharField(max_length=100, choices=[('chicken', 'Chicken on a stick > Raising Cane’s'), ('hammocks', 'The Circle should have hammocks'), ('vibes', 'You don’t need a planner — just vibes')])
    planner_fullness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True)  # Range 0-100%
    social_energy = models.CharField(max_length=50, choices=[('high', '📈 high'), ('low', '📉 low'), ('medium', '📊 mid')])
    major_approach = models.CharField(max_length=50, choices=[('love', 'I chose it because I love it'), ('career', 'It aligns with my career goals'), ('realistic', 'It was the most realistic option'), ('figuring_out', 'Still figuring it out 🤷')])
    post_grad_plan = models.CharField(max_length=50, choices=[('grad_school', '🎓 Grad school'), ('job', '💼 Job right away'), ('travel', '✈️ Take time off/travel'), ('unsure', '🤔 Still figuring it out')])
    college_motivation = models.CharField(max_length=50, choices=[('career', '🚀 Career success'), ('learning', '🧠 Learning new stuff'), ('prove', '🧍 Proving it to myself'), ('people', '👫 Meeting the right people')])
    campus_groups = models.CharField(max_length=100, choices=CAMPUS_GROUP_CHOICES)
    match_involvement_importance = models.CharField(max_length=50, choices=[('super', 'Super important'), ('little', 'A little'), ('doesnt_matter', 'Doesn’t matter'), ('prefer_not', 'I’d rather they weren’t 🤣')])
    social_energy_on_campus = models.CharField(max_length=50, choices=[('everywhere', 'I’m everywhere — love meeting people'), ('crew', 'I’ve got my crew, but I’m open'), ('low_key', 'Mostly low-key or solo'), ('searching', 'Still trying to find my people')])
    # Questionnaire end
    # -----------------
    # Questionnaire end


    gender = models.CharField(max_length=6, choices=GENDER_CHOICES_1, null=False, blank=False)

    preferred_gender = models.CharField(max_length=6, choices=GENDER_CHOICES_2, null=True, blank=True)

    # Additional fields
    hobbies = models.TextField(blank=True, null=True)
    clubs_and_extracurriculars = models.TextField(blank=True, null=True)
    # Profile Picture (Required)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default_profile_pic.jpg', blank=False, null=False)
    cover_photo = models.ImageField(upload_to='cover_photos/', default='default_profile_pic.jpg', blank=False, null=False)




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