from django.contrib import messages
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .utils import *
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render
from .models import Profile, FriendRequest, Chat, Message

# Third-party imports
import os
import json

# Local application imports
from .forms import *
from .models import *
import os
from django.db.models import Q
import json
from django.conf import settings
from app.utils import is_group_admin, is_super_admin
from .decorators import admin_required

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
            
            # Check if the user has a profile and if the first name is filled
            if hasattr(user, 'profile'):
                if not user.profile.first_name:  # Check if first_name is empty
                    return redirect('create_profile')
            
            # Redirect to home if the user has a profile with a first name
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
        return render(request, "home.html", {"profile": None})

    # Get liked and disliked profiles
    liked_profiles = user_profile.liked_profiles.values_list("id", flat=True)
    disliked_profiles = user_profile.disliked_profiles.values_list("id", flat=True)

    # Sent requests
    sent_requests = FriendRequest.objects.filter(sender=request.user, accepted=False).values_list("receiver__profile__id", flat=True)

    # Received requests
    received_requests = FriendRequest.objects.filter(receiver=request.user, accepted=False)
    pending_requests = [getattr(req.sender, 'profile', None) for req in received_requests if hasattr(req.sender, 'profile')]
    pending_request_ids = [profile.id for profile in pending_requests if profile]

    # Friends
    friends = user_profile.friends.all()
    friend_ids = friends.values_list('id', flat=True)

    # Filter profiles
    profiles = Profile.objects.exclude(user=request.user) \
        .exclude(id__in=liked_profiles) \
        .exclude(id__in=disliked_profiles) \
        .exclude(id__in=sent_requests) \
        .exclude(id__in=pending_request_ids) \
        .exclude(id__in=friend_ids)

    matches = find_study_partners(request.user)
    current_match = matches[:1] if matches else []

    # Fetch chats and associated messages
    chats = Chat.objects.filter(Q(user1=request.user) | Q(user2=request.user)).prefetch_related('messages')

    chat_data = []
    for chat in chats:
        friend = chat.user2 if chat.user1 == request.user else chat.user1
        messages = chat.messages.order_by('created_at')  # Messages related to the chat
        chat_data.append({
            'chat': chat,
            'friend': friend,
            'messages': messages,
            'chat_id': chat.id, # Make sure to include the chat_id in the context
        })

    return render(request, "home.html", {
        "profiles": profiles,
        "profile": user_profile,
        "pending_requests": pending_requests,
        "pending_request_ids": pending_request_ids,
        "friends": friends,
        "sent_requests": sent_requests,
        "matches": current_match,
        "chats": chat_data
    })

@login_required
def next_match(request):
    user_profile = Profile.objects.get(user=request.user)
    matches = find_study_partners(request.user)

    if matches:
        next_match = matches[1:2]  # Get the next match
        if next_match:
            return JsonResponse({
                "username": next_match[0].user.username,
                "subjects": next_match[0].subjects,
            })
    return JsonResponse({"error": "No more matches available."})


def logout_view(request):
    logout(request)
    return redirect("landing")

def landing(request):
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
    # Check if the user already has a profile
    try:
        profile = request.user.profile
        
        # If the user has a profile, check if the first name is missing
        if not profile.first_name:
            if request.method == "POST":
                form = ProfileForm(request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    form.save()  # Save the updated profile
                    return redirect("home")  # Redirect to the home page after saving
                else:
                    # If form is invalid, re-render the form with errors
                    return render(request, "create_profile.html", {"form": form})
            else:
                # If it's a GET request, display the existing profile form with data
                form = ProfileForm(instance=profile)
                return render(request, "create_profile.html", {"form": form})
        
        # If the user already has a complete profile, redirect to the home page
        return redirect("home")
    except Profile.DoesNotExist:
        # If the profile doesn't exist, continue with profile creation
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user  # Assign the current user to the profile
                profile.save()
                form.save_m2m()  # Save many-to-many relationships
                return redirect("home")  # Redirect to home page after profile creation
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

    # Check if sender already sent a request
    if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
        return JsonResponse({'success': False, 'message': "Friend request already sent."})

    # Check if receiver already sent a request to sender
    if FriendRequest.objects.filter(sender=receiver, receiver=sender).exists():
        return JsonResponse({'success': False, 'message': "This user already sent you a friend request."})

    # Check if already friends
    sender_profile = Profile.objects.get(user=sender)
    if receiver.profile in sender_profile.friends.all():
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

            # Ensure a chat room is created for the two users if it doesn't already exist
            chat_room = Chat.objects.filter(
                Q(user1=request.user, user2=sender_profile.user) |
                Q(user1=sender_profile.user, user2=request.user)
            ).first()

            if not chat_room:
                # If no chat exists, create one
                chat_room = Chat.objects.create(user1=request.user, user2=sender_profile.user)

            # Delete the friend request after acceptance
            friend_request.delete()

            return JsonResponse({
                "success": True,
                "message": "Friend request accepted and chat room created!",
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
            sender_profile = friend_request.sender.profile
            receiver_profile = request.user.profile

            # BOTH users dislike each other
            receiver_profile.disliked_profiles.add(sender_profile)
            sender_profile.disliked_profiles.add(receiver_profile)

            # Delete the friend request
            friend_request.delete()

            return JsonResponse({"success": True, "message": "Friend request declined!", "profile_id": profile_id})

        return JsonResponse({"success": False, "message": "No pending friend request from this user."})

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


from django.contrib import messages  # Ensure you import messages

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # Make sure the user is a participant
    if request.user not in [chat.user1, chat.user2]:
        return redirect('home')  # or show an error

    other_user = chat.user1 if chat.user2 == request.user else chat.user2
    messages = chat.messages.order_by('created_at')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()

            # messages.success(request, "Your message has been sent!")  # Correct usage of messages

            return redirect('chat', chat_id=chat.id)  # Redirect to the chat URL
    else:
        form = MessageForm()

    return render(request, 'chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'form': form,
        'other_user': other_user,
    })



@login_required
def send_message(request, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)

        # Check if the user is a participant of the chat
        if request.user != chat.user1 and request.user != chat.user2:
            return JsonResponse({"success": False, "message": "You are not a participant in this chat."})

        if request.method == "POST":
            message_content = request.POST.get("message")

            if message_content:
                # Create a new message object
                message = Message.objects.create(
                    chat=chat,
                    sender=request.user,
                    content=message_content
                )
                return JsonResponse({
                    "success": True,
                    "message": "Message sent!",
                    "message_content": message.content,
                    "sender_username": message.sender.username,
                    "created_at": message.created_at
                })

            return JsonResponse({"success": False, "message": "Message content is empty."})

        return JsonResponse({"success": False, "message": "Invalid request method."})

    except Chat.DoesNotExist:
        return JsonResponse({"success": False, "message": "Chat not found."})

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
    
def calendar(request):
    if not Event.objects.exists():
        json_file_path = os.path.join(settings.BASE_DIR, 'data', 'events.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                events_data = json.load(file)
                for event_data in events_data:
                    start_date = event_data['start_date']
                    end_date = event_data.get('end_date', start_date)
                    Event.objects.create(
                        title=event_data['title'],
                        start_date=start_date,
                        end_date=end_date,
                        days=event_data['days']
                    )

    events = Event.objects.all()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save()
            return JsonResponse({
                'success': True,
                'event': {
                    'title': new_event.title,
                    'start_date': new_event.start_date,
                    'end_date': new_event.end_date,
                    'days': new_event.days
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'Form is not valid'})

    else:
        form = EventForm()

    return render(request, 'calendar.html', {'events': events, 'form': form})


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})


# Custom decorator to check if the user is either a super admin or group admin
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is either a super admin or a group admin
        if not (is_super_admin(request.user) or is_group_admin(request.user)):
            return HttpResponseForbidden("You don't have permission to create a post.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# View to create a group post (both super admins and group admins can create posts)
@admin_required
def create_group_post(request):
    if request.method == 'POST':
        form = GroupPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('group_post_list')
    else:
        form = GroupPostForm()
    return render(request, 'create_post.html', {'form': form})

# View to delete a group post (super admins can delete any post, group admins can delete their own posts)
@login_required
def delete_group_post(request, post_id):
    post = get_object_or_404(GroupPost, id=post_id)
    
    # Check permissions: super admin can delete any post, group admin can only delete their own posts
    if request.user.profile.is_super_admin or (request.user.profile.is_group_admin and post.created_by == request.user):
        post.delete()
        return redirect('group_post_list')  # Redirect to the list after deletion
    else:
        return HttpResponseForbidden("You don't have permission to delete this post.")

# View to list all group posts
@login_required
def group_post_list(request):
    # Check if the user has a profile
    if not hasattr(request.user, 'profile'):
        return redirect('create_profile')  # Redirect to the profile creation page

    # Fetch the group posts
    posts = GroupPost.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

