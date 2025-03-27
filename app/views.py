from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomSignupForm, ProfileForm
from .models import Profile, Class

def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")  # Redirect to login after signup
    else:
        form = CustomSignupForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect("home")  # Redirect to the home page or logged-in page
        else:
            # If authentication fails, add an error message
            messages.error(request, "Invalid credentials! Please try again.")
            return render(request, "login.html")  # Render the login page with error message

    return render(request, "login.html")  # Render login page on GET request

@login_required
def home(request):
    # Check if the user has a profile
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None

    # If no profile, return home with no profile
    if not user_profile:
        return render(request, "home.html", {"profile": None})

    # Get profiles that the user hasn't interacted with
    liked_profiles = user_profile.liked_profiles.values_list("id", flat=True)
    disliked_profiles = user_profile.disliked_profiles.values_list("id", flat=True)

    profiles = Profile.objects.exclude(user=request.user).exclude(id__in=liked_profiles).exclude(id__in=disliked_profiles)

    return render(request, "home.html", {"profiles": profiles, "profile": user_profile})

def logout_view(request):
    logout(request)
    return redirect("index")

def index(request):
    return render(request, "landing.html")

@login_required
def like_profile(request, profile_id):
    """Handles liking a profile"""
    user_profile = Profile.objects.get(user=request.user)
    liked_profile = get_object_or_404(Profile, id=profile_id)

    user_profile.liked_profiles.add(liked_profile)
    return JsonResponse({"status": "liked"})

@login_required
def dislike_profile(request, profile_id):
    """Handles disliking a profile"""
    user_profile = Profile.objects.get(user=request.user)
    disliked_profile = get_object_or_404(Profile, id=profile_id)

    user_profile.disliked_profiles.add(disliked_profile)
    return JsonResponse({"status": "disliked"})

@login_required
def create_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)  # Ensure to include request.FILES for file uploads
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Link profile to logged-in user
            profile.save()
            form.save_m2m()  # Save many-to-many relationships (classes)
            return redirect("home")  # Redirect to home after profile creation
        else:
            # If form is not valid, include the error messages in the context
            return render(request, "create_profile.html", {"form": form})
    else:
        form = ProfileForm()

    return render(request, "create_profile.html", {"form": form})
