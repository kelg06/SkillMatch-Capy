def is_super_admin(user):
    return hasattr(user, 'profile') and user.profile.is_super_admin

def is_group_admin(user):
    return hasattr(user, 'profile') and user.profile.is_group_admin
