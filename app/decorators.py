from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from app.utils import is_group_admin, is_super_admin


# Redirect if already logged in
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Change 'home' to your homepage route name if needed
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def admin_required(view_func):
    @wraps(view_func)
    @login_required  # Ensures only logged-in users go through
    def _wrapped_view(request, *args, **kwargs):
        if not (is_super_admin(request.user) or is_group_admin(request.user)):
            return HttpResponseForbidden("You don't have permission to create a post.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view