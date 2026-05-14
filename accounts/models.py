"""accounts app 的数据模型。"""
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """扩展 Django 内置 User，保存 EventNow 需要的用户角色。

    这里不自定义 User model，是为了继续使用 Django 已经提供好的
    authentication、admin 和 permission 基础功能。
    """

    class Role(models.TextChoices):
        ATTENDEE = "attendee", "Attendee"
        ORGANISER = "organiser", "Organiser"
        ADMIN = "admin", "Admin"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ATTENDEE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
