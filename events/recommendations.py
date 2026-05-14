"""Rule-based event recommendation helpers for EventNow."""
from django.utils import timezone

from .models import Event, Registration, SessionSelection


def get_event_registered_count(event):
    """统计 event 当前有效报名人数；cancelled 不占用容量。"""
    return Registration.objects.filter(event=event, status=Registration.Status.REGISTERED).count()


def get_event_remaining_capacity(event):
    """计算 event 剩余总报名容量。"""
    return max(event.capacity - get_event_registered_count(event), 0)


def session_has_remaining_capacity(session):
    """判断 session 是否还有可选名额，只统计 active registrations。"""
    selected_count = SessionSelection.objects.filter(
        session=session,
        registration__status=Registration.Status.REGISTERED,
    ).count()
    return selected_count < session.capacity


def get_recommended_events(user, limit=10):
    """为已登录用户推荐 published events。

    推荐分数是可解释的 rule-based scoring：
    category match +5，organisation match +3，event/session 有容量各 +2，
    未来 14 天内开始 +1。
    """
    registered_event_ids = list(
        Registration.objects.filter(user=user, status=Registration.Status.REGISTERED).values_list(
            "event_id",
            flat=True,
        )
    )
    history = (
        Registration.objects.filter(user=user)
        .select_related("event__category", "event__organisation")
        .exclude(status=Registration.Status.CANCELLED)
    )
    preferred_category_ids = {
        registration.event.category_id for registration in history if registration.event.category_id
    }
    preferred_organisation_ids = {
        registration.event.organisation_id for registration in history if registration.event.organisation_id
    }
    has_history = bool(preferred_category_ids or preferred_organisation_ids)

    today = timezone.localdate()
    next_14_days = today + timezone.timedelta(days=14)
    events = (
        Event.objects.filter(status=Event.Status.PUBLISHED)
        .exclude(id__in=registered_event_ids)
        .select_related("category", "organisation", "venue")
        .prefetch_related("sessions")
        .order_by("start_datetime")
    )

    recommendations = []
    for event in events:
        remaining_capacity = get_event_remaining_capacity(event)
        if remaining_capacity <= 0:
            continue

        sessions = list(event.sessions.all())
        if not sessions or not any(session_has_remaining_capacity(session) for session in sessions):
            continue

        score = 0
        reasons = []

        if event.category_id in preferred_category_ids:
            score += 5
            reasons.append("Similar category")

        if event.organisation_id in preferred_organisation_ids:
            score += 3
            reasons.append("Same organiser organisation")

        score += 2
        reasons.append("Available event capacity")

        score += 2
        reasons.append("Available session capacity")

        event_date = timezone.localtime(event.start_datetime).date()
        if today <= event_date <= next_14_days:
            score += 1
            reasons.append("Starts within 14 days")

        if not has_history:
            reasons = ["Available upcoming event"]

        recommendations.append(
            {
                "event": event,
                "score": score,
                "reasons": reasons,
                "remaining_capacity": remaining_capacity,
            }
        )

    recommendations.sort(key=lambda item: (-item["score"], item["event"].start_datetime))
    return recommendations[:limit]
