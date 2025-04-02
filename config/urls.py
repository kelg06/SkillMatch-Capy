from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", startup, name="startup"),
    path("home/", home, name="home"),


    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path('accept-friend-request/<int:profile_id>/', accept_friend_request, name='accept_friend_request'),
    path('decline-friend-request/<int:profile_id>/', decline_friend_request, name='decline_friend_request'),
    path('send-friend-request/<int:profile_id>/', send_friend_request, name='send_friend_request'),

    path('chat/<str:chat_partner_username>/', chat_view, name='chat'),

    path("create-profile/", create_profile, name="create_profile"),
    path('update-profile/<int:profile_id>/', update_profile, name='update_profile'),
    path('delete-profile/<int:profile_id>/', delete_profile, name='delete_profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
