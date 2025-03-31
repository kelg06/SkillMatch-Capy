from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Class, Chat

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

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=True, widget=forms.Textarea(attrs={"placeholder": "Tell us about yourself"}))
    age = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"placeholder": "Enter your age"}))
    study_times = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "e.g. 10 AM - 2 PM"}))
    classes = forms.ModelMultipleChoiceField(
        queryset=Class.objects.all(),
        required=False,
        widget=forms.SelectMultiple()
    )
    profile_picture = forms.ImageField(required=True, error_messages={'required': 'Please upload a profile picture.'})

    class Meta:
        model = Profile
        fields = ["bio", "age", "study_times", "classes", "profile_picture"]

class ChatForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Type a message..."}))

    class Meta:
        model = Chat
        fields = ['message']
