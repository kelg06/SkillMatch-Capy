from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *

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

from django import forms
from .models import Profile

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
    
    # Study Times (Dropdown with predefined choices)
    study_times = forms.ChoiceField(
        choices=Profile.STUDY_TIME_CHOICES,
        required=True,
        widget=forms.Select(attrs={"class": "form-control form-field"})
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
            "first_name", "last_name", "age", "hometown", "major", 
            "minor", "grade", "study_times", "hobbies", 
            "clubs_and_extracurriculars", "goals_after", "profile_picture"
        ]


class ChatForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Type a message..."}))

    class Meta:
        model = Chat
        fields = ['message']

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