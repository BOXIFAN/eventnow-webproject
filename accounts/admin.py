"""accounts app 的 Django admin 配置。"""
from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """在 admin 中管理用户角色资料。"""

    list_display = ("user", "role", "created_at", "updated_at")
    list_filter = ("role", "created_at")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    ordering = ("user__username",)
