from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomSignupForm, ProfileForm
from django.views.decorators.http import require_POST
from .models import *

def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
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
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again.")
            return render(request, "login.html")

    return render(request, "login.html")

@login_required
def home(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = None

    if not user_profile:
        return render(request, "home.html", {"profile": None})


    liked_profiles = user_profile.liked_profiles.values_list("id", flat=True)
    disliked_profiles = user_profile.disliked_profiles.values_list("id", flat=True)


    sent_requests = FriendRequest.objects.filter(sender=request.user).values_list("receiver__profile__id", flat=True)


    received_requests = FriendRequest.objects.filter(receiver=request.user, accepted=False)

    profiles = Profile.objects.exclude(user=request.user).exclude(id__in=liked_profiles).exclude(id__in=disliked_profiles).exclude(id__in=sent_requests)

    friends = user_profile.friends.all()

    pending_requests = [getattr(req.sender, 'profile', None) for req in received_requests if hasattr(req.sender, 'profile')]


    print("Pending friend requests:", pending_requests)

    return render(request, "home.html", {
        "profiles": profiles,
        "profile": user_profile,
        "pending_requests": pending_requests,
        "friends": friends,
        "sent_requests": sent_requests,
    })



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
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()
            return redirect("home")
        else:
            return render(request, "create_profile.html", {"form": form})
    else:
        form = ProfileForm()

    return render(request, "create_profile.html", {"form": form})

@csrf_exempt
@login_required
def send_friend_request(request, profile_id):
    receiver = User.objects.get(id=profile_id)
    sender = request.user
    if sender == receiver:
        return JsonResponse({'success': False, 'message': "You can't send a friend request to yourself."})
    
    # Check if a request already exists
    if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
        return JsonResponse({'success': False, 'message': "Friend request already sent."})
    
    # Check if they are already friends
    sender_profile = Profile.objects.get(user=sender)
    if receiver in sender_profile.friends.all():
        return JsonResponse({'success': False, 'message': "You are already friends."})
    
    # Create friend request
    FriendRequest.objects.create(sender=sender, receiver=receiver)
    return JsonResponse({'success': True, 'message': "Friend request sent."})



@login_required
def accept_friend_request(request, profile_id):
    try:
        sender_profile = Profile.objects.get(id=profile_id)
        receiver_profile = request.user.profile

        # Find the friend request where the logged-in user is the receiver
        friend_request = FriendRequest.objects.filter(
            sender=sender_profile.user,
            receiver=request.user,
            accepted=False
        ).first()

        if friend_request:
            # Update the friend request to accepted and save
            friend_request.accepted = True
            friend_request.save()

            # Add each other as friends
            receiver_profile.friends.add(sender_profile)
            sender_profile.friends.add(receiver_profile)

            # Delete the friend request after acceptance
            friend_request.delete()

            print(f"Accepted friend request from {sender_profile.user.username}")
            return JsonResponse({
                "success": True, 
                "message": "Friend request accepted!", 
                "friend_username": sender_profile.user.username,
                "profile_id": profile_id
            })

        return JsonResponse({"success": False, "message": "No pending friend request from this user."})

    except Profile.DoesNotExist:
        return JsonResponse({"success": False, "message": "Profile not found."}, status=404)





@login_required
def decline_friend_request(request, profile_id):
    try:
        # Find the friend request where the logged-in user is the receiver
        friend_request = FriendRequest.objects.filter(
            sender__profile__id=profile_id,
            receiver=request.user,
            accepted=False
        ).first()

        if friend_request:
            # Delete the friend request from the database
            friend_request.delete()
            print(f"Declined friend request from profile ID {profile_id}")
            return JsonResponse({"success": True, "message": "Friend request declined!", "profile_id": profile_id})

        return JsonResponse({"success": False, "message": "No pending friend request from this user."})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


def chat_view(request, chat_partner_username):

    try:
        chat_partner = User.objects.get(username=chat_partner_username)
    except User.DoesNotExist:
        messages.error(request, f"User {chat_partner_username} not found")
        return redirect('some_fallback_url')
    chat_room, created = Chat.objects.get_or_create(
        user1=request.user, user2=chat_partner
    )

    if created:
        print(f"New chat room created between {request.user.username} and {chat_partner.username}")
    context = {
        'chat_partner': chat_partner,
        'user': request.user,
        'chat_room': chat_room,
    }

    return render(request, 'chat.html', context)

@login_required
def update_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)

    if request.method == "POST":
        profile.first_name = request.POST.get("first_name", profile.first_name)
        profile.last_name = request.POST.get("last_name", profile.last_name)
        profile.age = request.POST.get("age", profile.age)
        profile.hometown = request.POST.get("hometown", profile.hometown)
        profile.major = request.POST.get("major", profile.major)
        profile.minor = request.POST.get("minor", profile.minor)
        profile.grade = request.POST.get("grade", profile.grade)
        profile.study_times = request.POST.get("study_times", profile.study_times)
        profile.hobbies = request.POST.get("hobbies", profile.hobbies)
        profile.clubs_and_extracurriculars = request.POST.get("clubs_and_extracurriculars", profile.clubs_and_extracurriculars)
        profile.goals_after = request.POST.get("goals_after", profile.goals_after)

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("home")

    return render(request, "update_profile.html", {"profile": profile})


@login_required
def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)

    if request.method == "POST":
        profile.delete()
        messages.success(request, "Profile deleted successfully!")
        return redirect("home")

    return render(request, "delete_profile.html", {"profile": profile})

@login_required
def unfriend(request, profile_id):
    try:
        user_profile = request.user.profile
        friend_profile = Profile.objects.get(id=profile_id)

        # Remove the friend relationship both ways
        if friend_profile in user_profile.friends.all():
            user_profile.friends.remove(friend_profile)
            friend_profile.friends.remove(user_profile)

        print(f"Unfriended {friend_profile.user.username}")
        return JsonResponse({"success": True, "message": "Unfriended successfully!"})

    except Profile.DoesNotExist:
        return JsonResponse({"success": False, "message": "Friend not found."}, status=404)












