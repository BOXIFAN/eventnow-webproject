"""events app 的 Django admin 配置。"""
from django.contrib import admin

from .models import Category, Event, Registration, SavedEvent, Session, SessionSelection, Venue


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """在 admin 中管理 event 分类。"""

    list_display = ("name", "created_at", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    """在 admin 中管理 venue。"""

    list_display = ("name", "city", "room", "created_at")
    list_filter = ("city",)
    search_fields = ("name", "address", "city", "room")
    ordering = ("city", "name")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """在 admin 中管理 events。"""

    list_display = (
        "title",
        "organiser",
        "organisation",
        "status",
        "start_datetime",
        "capacity",
        "price",
    )
    list_filter = ("status", "category", "organisation")
    search_fields = ("title", "description")
    ordering = ("-start_datetime",)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """在 admin 中管理 event sessions。"""

    list_display = ("title", "event", "start_datetime", "capacity")
    list_filter = ("event",)
    search_fields = ("title", "description", "event__title")
    ordering = ("start_datetime",)


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """在 admin 中管理 event registrations。"""

    list_display = ("event", "user", "status", "created_at")
    list_filter = ("status", "event")
    search_fields = ("event__title", "user__username", "user__email")
    ordering = ("-created_at",)


@admin.register(SessionSelection)
class SessionSelectionAdmin(admin.ModelAdmin):
    """在 admin 中管理用户选择的 sessions。"""

    list_display = ("registration", "session", "created_at")
    list_filter = ("session", "created_at")
    search_fields = ("registration__user__username", "session__title", "session__event__title")
    ordering = ("-created_at",)


@admin.register(SavedEvent)
class SavedEventAdmin(admin.ModelAdmin):
    """在 admin 中管理用户保存的 events。"""

    list_display = ("user", "event", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "user__email", "event__title")
    ordering = ("-created_at",)
