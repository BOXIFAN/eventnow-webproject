"""accounts app 的页面视图。"""
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .decorators import get_user_role
from .forms import RegisterForm
from .models import UserProfile


def login_view(request):
    """处理用户登录，并根据角色跳转到合适页面。"""
    if request.user.is_authenticated:
        return redirect("accounts:dashboard_redirect")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have logged in successfully.")
            return redirect("accounts:dashboard_redirect")

        messages.error(request, "Login failed. Please check your username and password.")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    """处理用户注册；注册成功后自动登录。"""
    if request.user.is_authenticated:
        return redirect("accounts:dashboard_redirect")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 注册时已经创建 UserProfile，这里自动登录提升用户体验。
            login(request, user)
            messages.success(request, "Your account has been created successfully.")
            return redirect("accounts:dashboard_redirect")

        messages.error(request, "Registration failed. Please review the form below.")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    """退出当前用户并回到首页。"""
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("home")


def dashboard_redirect_view(request):
    """根据用户角色跳转到对应 dashboard 或列表页面。"""
    role = get_user_role(request.user)

    # role redirect 集中放在这里，后续新增 dashboard 时只需要改一个地方。
    if request.user.is_superuser or role == UserProfile.Role.ADMIN:
        return redirect("subscriptions:subscription_list")

    if role == UserProfile.Role.ORGANISER:
        return redirect("events:organiser_dashboard")

    return redirect("events:event_list")
