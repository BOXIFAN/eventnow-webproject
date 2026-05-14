"""subscriptions app 的 Django admin 配置。"""
from django.contrib import admin

from .models import Organisation, Subscription


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    """在 admin 中管理 organisation。"""

    list_display = ("name", "owner", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description", "owner__username", "owner__email")
    ordering = ("name",)


@admin.action(description="Archive selected subscriptions")
def archive_selected_subscriptions(modeladmin, request, queryset):
    """将选中的 subscriptions 标记为 archived，而不是真正删除。"""
    queryset.update(status=Subscription.Status.ARCHIVED)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """在 admin 中管理 SaaS subscriptions。"""

    list_display = ("organisation", "plan_name", "status", "start_date", "end_date")
    list_filter = ("status", "plan_name", "start_date", "end_date")
    search_fields = ("organisation__name", "plan_name")
    ordering = ("-start_date",)
    actions = (archive_selected_subscriptions,)
