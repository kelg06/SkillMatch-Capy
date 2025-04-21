from django.urls import path
from django.contrib import admin
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('contact/', contact_view,name='contact'),
    path('next-match/', next_match, name='next_match'),
    path('create-profile/', create_profile, name='create_profile'),
    path('accept-friend-request/<int:profile_id>/', accept_friend_request, name='accept_friend_request'),
    path('decline-friend-request/<int:profile_id>/', decline_friend_request, name='decline_friend_request'),
    path('send-friend-request/<int:profile_id>/', send_friend_request, name='send_friend_request'),
    path("swipe-profile/<int:profile_id>/", swipe_profile, name="swipe_profile"),
    path('chat/<int:chat_id>/send_message/', send_message, name='send_message'),
    path('update-profile/<int:profile_id>/', update_profile, name='update_profile'),
    path('chat/<int:chat_id>/', chat_detail, name='chat'),
    path('update-profile/<int:profile_id>/', update_profile, name='update_profile'),
    path('delete-profile/<int:profile_id>/', delete_profile, name='delete_profile'), 
    path('unfriend/<int:profile_id>/', unfriend, name='unfriend'),
    path('calendar/', calendar, name='calendar'),
    path('group-posts/', group_post_list, name='group_post_list'),
    path('group-posts/create/', create_group_post, name='create_group_post'),
    path('group-posts/delete/<int:post_id>/', delete_group_post, name='delete_group_post'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)