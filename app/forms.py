from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django import forms
from .models import Profile


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'grove_or_game_day', 'ideal_study_spot', 'study_time', 
            'energy_source', 'personality_label', 'group_project_role', 
            'personal_motto', 'exam_prep_style', 'productivity_time', 
            'academic_strength', 'accountability_style', 'weekend_vibe', 
            'meet_people', 'wish_more_of', 'favorite_tradition', 
            'hot_take', 'secret_campus_hack', 'todays_vibe', 
            'planner_fullness', 'social_energy', 'ghost_likelihood', 
            'major_approach', 'post_grad_plan', 'college_motivation', 
            'campus_groups', 'match_involvement_importance',
            'social_energy_on_campus'
        ]
        widgets = {
            'grove_or_game_day': forms.Select(attrs={'class': 'form-control'}),
            'ideal_study_spot': forms.Select(attrs={'class': 'form-control'}),
            'study_time': forms.Select(attrs={'class': 'form-control'}),
            'energy_source': forms.Select(attrs={'class': 'form-control'}),
            'personality_label': forms.Select(attrs={'class': 'form-control'}),
            'group_project_role': forms.Select(attrs={'class': 'form-control'}),
            'personal_motto': forms.Select(attrs={'class': 'form-control'}),
            'exam_prep_style': forms.Select(attrs={'class': 'form-control'}),
            'productivity_time': forms.Select(attrs={'class': 'form-control'}),
            'academic_strength': forms.Select(attrs={'class': 'form-control'}),
            'accountability_style': forms.Select(attrs={'class': 'form-control'}),
            'weekend_vibe': forms.Select(attrs={'class': 'form-control'}),
            'meet_people': forms.Select(attrs={'class': 'form-control'}),
            'wish_more_of': forms.Select(attrs={'class': 'form-control'}),
            'favorite_tradition': forms.Select(attrs={'class': 'form-control'}),
            'hot_take': forms.Select(attrs={'class': 'form-control'}),
            'secret_campus_hack': forms.Textarea(attrs={'class': 'form-control'}),
            'todays_vibe': forms.Select(attrs={'class': 'form-control'}),
            'planner_fullness': forms.NumberInput(attrs={'class': 'form-control'}),
            'social_energy': forms.Select(attrs={'class': 'form-control'}),
            'ghost_likelihood': forms.Select(attrs={'class': 'form-control'}),
            'major_approach': forms.Select(attrs={'class': 'form-control'}),
            'post_grad_plan': forms.Select(attrs={'class': 'form-control'}),
            'college_motivation': forms.Select(attrs={'class': 'form-control'}),
            'campus_groups': forms.Select(attrs={'class': 'form-control'}),
            'match_involvement_importance': forms.Select(attrs={'class': 'form-control'}),
            'social_energy_on_campus': forms.Select(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    # First Name (Required)
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name", "class": "form-control form-field"})
    )
    
    # Last Name (Required)
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your last name", "class": "form-control form-field"})
    )
    
    # Age (Required)
    age = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={"placeholder": "Enter your age", "class": "form-control form-field"})
    )

    gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES_1,
        required=False,
        widget=forms.Select(attrs={"class": "form-control form-field"})
    )
    
    preferred_gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES_2,
        required=False,
        widget=forms.Select(attrs={"class": "form-control form-field"})
    )

    # Hometown (Required)
    hometown = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your hometown", "class": "form-control form-field"})
    )
    
    # Major (Required)
    major = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Enter your major", "class": "form-control form-field"})
    )
    
    # Minor (Optional)
    minor = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter your minor (optional)", "class": "form-control form-field"})
    )
    
    # Grade (Required)
    grade = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"placeholder":"freshman,Junior ex.", "class": "form-control form-field"})
    )
    
    # Hobbies (Optional)
    hobbies = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "Tell us about your hobbies (optional)", "class": "form-control form-field"})
    )
    
    # Clubs and Extracurriculars (Optional)
    clubs_and_extracurriculars = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"placeholder": "Tell us about your clubs and extracurricular activities (optional)", "class": "form-control form-field"})
    )
    
    # Goals After Graduation (Required)
    goals_after = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "What are your goals after graduation?", "class": "form-control form-field"})
    )
    
    # Profile Picture (Required)
    profile_picture = forms.ImageField(
        required=True,
        error_messages={'required': 'Please upload a profile picture.'},
        widget=forms.ClearableFileInput(attrs={"class": "form-control form-field"})
    )
    
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'age', 'gender', 
            'preferred_gender', 'hometown', 
            'major', 'minor', 'grade', 
            'hobbies', 'clubs_and_extracurriculars', 
            'goals_after', 'profile_picture'
        ]

class CustomSignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=100, required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type your message here...'})
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_date', 'end_date', 'days']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ['title', 'image']


class ContactForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'First and Last Name'})
    )
    subject = forms.CharField(
        label='Subject',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Subject of your message'})
    )
    email = forms.EmailField(
        label='Your Email',
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'})
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'placeholder': 'Type your message here...'})
    )
