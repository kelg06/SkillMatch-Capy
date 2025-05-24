from django.contrib import admin
from .models import *

class GroupPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'updated_at')  # Add fields you want to display
    list_filter = ('created_by',)  # Optionally filter by who created the post
    search_fields = ('title', 'created_by__username')  # Search by title or username of creator
    readonly_fields = ('created_by', 'created_at', 'updated_at')  # Make certain fields readonly

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            return request.user.profile.is_super_admin
        except Profile.DoesNotExist:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            return request.user.profile.is_super_admin
        except Profile.DoesNotExist:
            return False


# Register GroupPost model with the admin site
admin.site.register(GroupPost, GroupPostAdmin)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'is_super_admin', 'is_group_admin')
    search_fields = ('user__username', 'first_name', 'last_name')
    readonly_fields = ('user',)

admin.site.register(Profile, ProfileAdmin)