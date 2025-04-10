from django.urls import path
from django.contrib import admin
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", landing, name="landing"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", home, name="home"),
    path('next-match/', next_match, name='next_match'),
    path("create-profile/", create_profile, name="create_profile"),
    path('accept-friend-request/<int:profile_id>/', accept_friend_request, name='accept_friend_request'),
    path('decline-friend-request/<int:profile_id>/', decline_friend_request, name='decline_friend_request'),
    path('send-friend-request/<int:profile_id>/', send_friend_request, name='send_friend_request'),
    path('chat/<str:chat_partner_username>/', chat_detail, name='chat'),
    path('chat/<int:chat_id>/send_message/', send_message, name='send_message'),
    path('update-profile/<int:profile_id>/', update_profile, name='update_profile'),
    path('chat/<int:chat_id>/', chat_detail, name='chat'),
    path('update-profile/<int:profile_id>/', update_profile, name='update_profile'),
    path('delete-profile/<int:profile_id>/', delete_profile, name='delete_profile'),
    path('delete-profile/<int:profile_id>/', delete_profile, name='delete_profile'),
    path('unfriend/<int:profile_id>/', unfriend, name='unfriend'),
    path('calendar/', calendar, name='calendar'),
    path('add-event/', add_event, name='add_event'),
    path('group-posts/', group_post_list, name='group_post_list'),
    path('group-posts/create/', create_group_post, name='create_group_post'),
    path('group-posts/delete/<int:post_id>/', delete_group_post, name='delete_group_post')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
