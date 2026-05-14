"""events app 的数据模型。"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    """Event 分类，例如 workshop、seminar、networking。"""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Venue(models.Model):
    """Event 或 session 所在地点。"""

    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    room = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.room:
            return f"{self.name} - {self.room}"
        return self.name


class Event(models.Model):
    """EventNow 的核心活动模型。"""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    organisation = models.ForeignKey(
        "subscriptions.Organisation",
        on_delete=models.CASCADE,
        related_name="events",
    )
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organised_events")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="events")
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to="event_images/",
        blank=True,
        null=True,
        help_text="event image 用于活动卡片和活动详情页展示，不是必填字段。",
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    # 免费活动价格保存为 0，不使用 null，方便之后做筛选和计算。
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """基础数据验证，避免保存明显不合理的 event。"""
        if self.end_datetime and self.start_datetime and self.end_datetime <= self.start_datetime:
            raise ValidationError("Event end datetime must be later than start datetime.")

        if self.capacity is not None and self.capacity <= 0:
            raise ValidationError("Event capacity must be greater than 0.")

        # price 必须大于等于 0；免费活动统一用 0，方便后续筛选和报表统计。
        if self.price is not None and self.price < 0:
            raise ValidationError("Price cannot be negative. Use 0 for free events.")

    def __str__(self):
        return self.title


class Session(models.Model):
    """Event 下的具体 session，例如不同时间段的讲座或 workshop。"""

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="sessions")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """基础数据验证，避免保存明显不合理的 session。"""
        if self.end_datetime and self.start_datetime and self.end_datetime < self.start_datetime:
            raise ValidationError("Session end datetime cannot be earlier than start datetime.")

        if self.capacity is not None and self.capacity <= 0:
            raise ValidationError("Session capacity must be greater than 0.")

    def __str__(self):
        return f"{self.event.title} - {self.title}"


class Registration(models.Model):
    """用户对 event 的报名记录。"""

    class Status(models.TextChoices):
        REGISTERED = "registered", "Registered"
        CANCELLED = "cancelled", "Cancelled"
        ATTENDED = "attended", "Attended"

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registrations")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REGISTERED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "user"], name="unique_event_registration"),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class SessionSelection(models.Model):
    """用户报名 event 后选择的 session。"""

    registration = models.ForeignKey(
        Registration,
        on_delete=models.CASCADE,
        related_name="session_selections",
    )
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="session_selections")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["registration", "session"],
                name="unique_session_selection",
            ),
        ]

    def __str__(self):
        return f"{self.registration.user.username} - {self.session.title}"


class SavedEvent(models.Model):
    """用户保存/收藏的 event。"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_events")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="saved_by_users")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "event"], name="unique_saved_event"),
        ]

    def __str__(self):
        return f"{self.user.username} saved {self.event.title}"
