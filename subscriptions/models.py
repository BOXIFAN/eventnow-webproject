"""subscriptions app 的数据模型。"""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Organisation(models.Model):
    """组织/公司信息，是 organiser 管理 events 的归属单位。"""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        REJECTED = "rejected", "Rejected"
        SUSPENDED = "suspended", "Suspended"
        ARCHIVED = "archived", "Archived"

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organisations")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def has_active_subscription(self):
        """subscription 控制 organisation 是否拥有当前平台使用资格。"""
        today = timezone.localdate()
        return (
            self.status == self.Status.ACTIVE
            and self.subscriptions.filter(
                status=Subscription.Status.ACTIVE,
                start_date__lte=today,
                end_date__gte=today,
            ).exists()
        )


class Subscription(models.Model):
    """组织的 SaaS subscription 记录。

    subscription 持有 organisation 外键，方便一个 organisation 后续拥有多段订阅历史。
    archive 通过 status 标记完成，不真正删除数据库记录。
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        ARCHIVED = "archived", "Archived"

    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    plan_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.organisation.name} - {self.plan_name}"

    def is_currently_active(self):
        """判断 subscription 当前是否在有效日期范围内。"""
        today = timezone.localdate()
        return self.status == self.Status.ACTIVE and self.start_date <= today <= self.end_date
