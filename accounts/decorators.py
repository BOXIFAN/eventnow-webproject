"""accounts app 的权限装饰器。"""
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import UserProfile


def get_user_role(user):
    """安全读取用户角色；如果没有 UserProfile，就默认当作 attendee。"""
    if not user.is_authenticated:
        return UserProfile.Role.ATTENDEE

    try:
        return user.userprofile.role
    except UserProfile.DoesNotExist:
        return UserProfile.Role.ATTENDEE


def organiser_required(view_func):
    """只允许 organiser、admin 或 superuser 访问 organiser 页面。"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        role = get_user_role(request.user)

        # superuser 视为最高权限，方便课程项目测试和后台管理。
        if request.user.is_superuser or role in [UserProfile.Role.ORGANISER, UserProfile.Role.ADMIN]:
            return view_func(request, *args, **kwargs)

        messages.error(request, "You need organiser access to view that page.")
        return redirect("events:event_list")

    return wrapper


def admin_required(view_func):
    """只允许 admin role 或 superuser 访问 admin-only 页面。"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        role = get_user_role(request.user)

        if request.user.is_superuser or role == UserProfile.Role.ADMIN:
            return view_func(request, *args, **kwargs)

        messages.error(request, "You need admin access to view that page.")
        return redirect("home")

    return wrapper
