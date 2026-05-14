"""events app 的页面视图。"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import get_user_role, organiser_required
from accounts.models import UserProfile
from subscriptions.models import Organisation

from .forms import EventForm, EventRegistrationForm, SessionForm
from .models import Category, Event, Registration, Session, SessionSelection
from .recommendations import get_recommended_events


def get_manageable_events_queryset(user):
    """返回当前用户可管理的 events queryset。"""
    if not user.is_authenticated:
        return Event.objects.none()

    role = get_user_role(user)
    if user.is_superuser or role == UserProfile.Role.ADMIN:
        return Event.objects.all()

    return Event.objects.filter(organisation__owner=user)


def can_manage_event(user, event):
    """判断当前用户是否可以管理某个 event。

    organiser 只能管理自己 organisation 下的 event；admin/superuser 可以管理所有 event。
    """
    if not user.is_authenticated:
        return False

    role = get_user_role(user)
    if user.is_superuser or role == UserProfile.Role.ADMIN:
        return True

    return event.organisation.owner_id == user.id


def can_write_event(user, event):
    """判断当前用户是否可以修改 event/session。

    subscription 失效后，organiser 保留历史查看权限，但失去 event/session 写权限。
    admin/superuser 不受 subscription 和 archived 状态限制。
    """
    if not can_manage_event(user, event):
        return False

    role = get_user_role(user)
    if user.is_superuser or role == UserProfile.Role.ADMIN:
        return True

    if event.status == Event.Status.ARCHIVED:
        return False

    return event.organisation.has_active_subscription()


def get_event_registered_count(event):
    """统计 event 当前有效报名人数。"""
    return Registration.objects.filter(event=event, status=Registration.Status.REGISTERED).count()


def get_session_selected_count(session):
    """统计 session 当前有效选择人数。"""
    return SessionSelection.objects.filter(
        session=session,
        registration__status=Registration.Status.REGISTERED,
    ).count()


def add_remaining_capacity_to_sessions(sessions):
    """给 session 对象临时加 remaining_capacity，方便 template 展示。"""
    for session in sessions:
        session.selected_count = get_session_selected_count(session)
        session.remaining_capacity = max(session.capacity - session.selected_count, 0)
    return sessions


def add_capacity_to_events(events):
    """给 event 对象临时加 active registration 和 remaining capacity 数据。"""
    for event in events:
        # 只统计 registered，因为 cancelled registration 保留历史但不占用容量。
        event.registered_count = get_event_registered_count(event)
        event.remaining_capacity = max(event.capacity - event.registered_count, 0)
        event.is_full = event.remaining_capacity <= 0
    return events


def add_write_access_to_events(events, user):
    """给 event 对象临时加 can_write/is_readonly，方便 template 隐藏写操作。"""
    for event in events:
        event.can_write = can_write_event(user, event)
        event.is_readonly = can_manage_event(user, event) and not event.can_write
    return events


def event_list(request):
    """公开 event 列表，只显示 published events。"""
    events = Event.objects.filter(status=Event.Status.PUBLISHED).select_related(
        "category",
        "venue",
        "organisation",
    )

    keyword = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()

    if keyword:
        events = events.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))

    if category_id:
        events = events.filter(category_id=category_id)

    context = {
        "events": events.order_by("start_datetime"),
        "categories": Category.objects.order_by("name"),
        "keyword": keyword,
        "selected_category": category_id,
    }
    return render(request, "events/event_list.html", context)


@login_required
def recommended_events(request):
    """显示基于用户报名历史和容量的推荐 events。"""
    recommendations = get_recommended_events(request.user)
    return render(request, "events/recommended_events.html", {"recommendations": recommendations})


def event_detail(request, event_id):
    """公开 event 详情；未发布 event 只允许 owner/admin/superuser 查看。"""
    event = get_object_or_404(
        Event.objects.select_related("category", "venue", "organisation", "organiser").prefetch_related("sessions"),
        pk=event_id,
    )

    if event.status != Event.Status.PUBLISHED and not can_manage_event(request.user, event):
        messages.error(request, "This event is not available for public viewing.")
        return redirect("events:event_list")

    sessions = add_remaining_capacity_to_sessions(list(event.sessions.all().order_by("start_datetime")))
    user_registration = None
    if request.user.is_authenticated:
        user_registration = Registration.objects.filter(event=event, user=request.user).first()

    context = {
        "event": event,
        "can_manage": can_manage_event(request.user, event),
        "can_write": can_write_event(request.user, event),
        "event_sessions": sessions,
        "event_remaining_capacity": max(event.capacity - get_event_registered_count(event), 0),
        "user_registration": user_registration,
        "user_role": get_user_role(request.user),
    }
    return render(request, "events/event_detail.html", context)


@login_required
@organiser_required
def organiser_dashboard(request):
    """显示 organiser workflow 入口。"""
    role = get_user_role(request.user)

    # admin/superuser 在 dashboard 中查看全平台数据；普通 organiser 只看自己的 events。
    if request.user.is_superuser or role == UserProfile.Role.ADMIN:
        events = Event.objects.all()
    else:
        events = get_manageable_events_queryset(request.user)

    events = events.prefetch_related("sessions")
    sessions = Session.objects.filter(event__in=events)
    active_registrations = Registration.objects.filter(
        event__in=events,
        status=Registration.Status.REGISTERED,
    )

    full_sessions_count = 0
    for session in sessions:
        if get_session_selected_count(session) >= session.capacity:
            full_sessions_count += 1

    owned_organisations = request.user.organisations.exclude(status=Organisation.Status.ARCHIVED)
    active_organisation = owned_organisations.filter(status=Organisation.Status.ACTIVE).first()
    pending_organisation = owned_organisations.filter(status=Organisation.Status.PENDING).first()
    rejected_organisation = owned_organisations.filter(status=Organisation.Status.REJECTED).first()

    context = {
        "event_count": events.count(),
        "active_registration_count": active_registrations.count(),
        "session_count": sessions.count(),
        "full_session_count": full_sessions_count,
        "is_admin_view": request.user.is_superuser or role == UserProfile.Role.ADMIN,
        "has_publishing_access": (
            request.user.is_superuser
            or role == UserProfile.Role.ADMIN
            or any(organisation.has_active_subscription() for organisation in request.user.organisations.all())
        ),
        "active_organisation": active_organisation,
        "pending_organisation": pending_organisation,
        "rejected_organisation": rejected_organisation,
        "has_any_organisation": owned_organisations.exists(),
    }
    return render(request, "events/organiser_dashboard.html", context)


@login_required
@organiser_required
def organiser_event_list(request):
    """显示当前 organiser 可以管理的 events。"""
    role = get_user_role(request.user)

    # admin/superuser 在管理页可以看到所有 events；普通 organiser 只看到自己 organisation 下的 events。
    events = get_manageable_events_queryset(request.user)

    status = request.GET.get("status", "").strip()
    if status:
        events = events.filter(status=status)

    events = add_capacity_to_events(
        list(events.select_related("organisation", "category", "venue").order_by("-start_datetime"))
    )
    events = add_write_access_to_events(events, request.user)

    context = {
        "events": events,
        "status": status,
        "status_choices": Event.Status.choices,
        "is_admin_view": request.user.is_superuser or role == UserProfile.Role.ADMIN,
        "has_publishing_access": (
            request.user.is_superuser
            or role == UserProfile.Role.ADMIN
            or any(organisation.has_active_subscription() for organisation in request.user.organisations.all())
        ),
    }
    return render(request, "events/organiser_event_list.html", context)


@login_required
@organiser_required
def event_create(request):
    """创建 event，organiser 自动设置为当前用户。"""
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, user=request.user)
        if not form.has_publishing_access:
            messages.error(
                request,
                "Your organisation does not have an active subscription. You can view existing records, but cannot create new events.",
            )
            return redirect("events:organiser_event_list")

        if form.is_valid():
            event = form.save(commit=False)
            # organiser 不能从表单选择，避免冒充其他用户创建 event。
            event.organiser = request.user
            if not request.user.is_superuser and get_user_role(request.user) != UserProfile.Role.ADMIN:
                if event.organisation.owner_id != request.user.id:
                    messages.error(request, "You can only create events for your own organisation.")
                    return redirect("events:organiser_event_list")
                if not event.organisation.has_active_subscription():
                    messages.error(
                        request,
                        "Your organisation does not have an active subscription. You can view existing records, but cannot create new events.",
                    )
                    return redirect("events:organiser_event_list")
            if not request.user.is_superuser and get_user_role(request.user) != UserProfile.Role.ADMIN:
                event.status = form.cleaned_data.get("status") or Event.Status.PENDING
            event.save()
            messages.success(request, "Event created successfully.")
            return redirect("events:organiser_event_list")

        messages.error(request, "Event creation failed. Please review the form.")
    else:
        form = EventForm(user=request.user)

    if not form.has_publishing_access:
        messages.warning(
            request,
            "Your organisation does not have an active subscription. You can view existing records, but cannot create new events.",
        )

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "page_title": "Create Event",
            "submit_label": "Save Event",
            "can_save_event": form.has_publishing_access,
        },
    )


@login_required
@organiser_required
def event_edit(request, event_id):
    """编辑 event；organiser 只能编辑自己 organisation 下的 event。"""
    event = get_object_or_404(Event, pk=event_id)

    if not can_manage_event(request.user, event):
        messages.error(request, "You can only edit events for your own organisation.")
        return redirect("events:organiser_event_list")

    if not can_write_event(request.user, event):
        messages.error(
            request,
            "This organisation does not have an active subscription. Existing events are read-only until the subscription is reactivated.",
        )
        return redirect("events:event_detail", event_id=event.id)

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event, user=request.user)
        if form.is_valid():
            # 保存 existing event 时不修改 organiser，避免把 ownership 改给别人。
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect("events:organiser_event_list")

        messages.error(request, "Event update failed. Please review the form.")
    else:
        form = EventForm(instance=event, user=request.user)

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "event": event,
            "page_title": "Edit Event",
            "submit_label": "Save Changes",
            "can_save_event": True,
        },
    )


@login_required
@organiser_required
def event_archive(request, event_id):
    """archive event，不真正删除数据库记录。"""
    event = get_object_or_404(Event, pk=event_id)

    if not can_manage_event(request.user, event):
        messages.error(request, "You can only archive events for your own organisation.")
        return redirect("events:organiser_event_list")

    if not can_write_event(request.user, event):
        messages.error(
            request,
            "This organisation does not have an active subscription. Existing events are read-only until the subscription is reactivated.",
        )
        return redirect("events:event_detail", event_id=event.id)

    if request.method == "POST":
        event.status = Event.Status.ARCHIVED
        event.save(update_fields=["status", "updated_at"])
        messages.success(request, "Event archived successfully.")
        return redirect("events:organiser_event_list")

    return render(request, "events/event_confirm_archive.html", {"event": event})


@login_required
@organiser_required
def session_list(request, event_id):
    """显示某个 event 下的 sessions。"""
    event = get_object_or_404(Event, pk=event_id)

    # organiser 只能查看自己 organisation event 下的 sessions；admin/superuser 可以管理全部。
    if not can_manage_event(request.user, event):
        messages.error(request, "You can only view sessions for events in your own organisation.")
        return redirect("events:organiser_event_list")

    sessions = event.sessions.order_by("start_datetime")
    context = {
        "event": event,
        "sessions": sessions,
        "can_write": can_write_event(request.user, event),
    }
    return render(request, "events/session_list.html", context)


@login_required
@organiser_required
def session_create(request, event_id):
    """为 URL 指定的 event 创建 session。"""
    event = get_object_or_404(Event, pk=event_id)

    if not can_manage_event(request.user, event):
        messages.error(request, "You can only create sessions for events in your own organisation.")
        return redirect("events:organiser_event_list")

    if not can_write_event(request.user, event):
        messages.error(
            request,
            "This organisation does not have an active subscription. Sessions are read-only until the subscription is reactivated.",
        )
        return redirect("events:session_list", event_id=event.id)

    if request.method == "POST":
        form = SessionForm(request.POST, event=event)
        if form.is_valid():
            session = form.save(commit=False)
            # event 不从表单选择，必须由 URL 中的 event_id 自动设置。
            session.event = event
            session.save()
            messages.success(request, "Session created successfully.")
            return redirect("events:session_list", event_id=event.id)

        messages.error(request, "Session creation failed. Please review the form.")
    else:
        form = SessionForm(event=event)

    context = {
        "form": form,
        "event": event,
        "page_title": "Create Session",
        "submit_label": "Save Session",
    }
    return render(request, "events/session_form.html", context)


@login_required
@organiser_required
def session_edit(request, session_id):
    """编辑 session；权限由 session 所属 event 决定。"""
    session = get_object_or_404(Session.objects.select_related("event"), pk=session_id)
    event = session.event

    if not can_manage_event(request.user, event):
        messages.error(request, "You can only edit sessions for events in your own organisation.")
        return redirect("events:organiser_event_list")

    if not can_write_event(request.user, event):
        messages.error(
            request,
            "This organisation does not have an active subscription. Sessions are read-only until the subscription is reactivated.",
        )
        return redirect("events:session_list", event_id=event.id)

    if request.method == "POST":
        form = SessionForm(request.POST, instance=session, event=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Session updated successfully.")
            return redirect("events:session_list", event_id=event.id)

        messages.error(request, "Session update failed. Please review the form.")
    else:
        form = SessionForm(instance=session, event=event)

    context = {
        "form": form,
        "event": event,
        "session": session,
        "page_title": "Edit Session",
        "submit_label": "Save Session",
    }
    return render(request, "events/session_form.html", context)


@login_required
@organiser_required
def session_delete(request, session_id):
    """删除 session；当前阶段 session 作为 event 子项允许真正删除。"""
    session = get_object_or_404(Session.objects.select_related("event"), pk=session_id)
    event = session.event

    if not can_manage_event(request.user, event):
        messages.error(request, "You can only delete sessions for events in your own organisation.")
        return redirect("events:organiser_event_list")

    if not can_write_event(request.user, event):
        messages.error(
            request,
            "This organisation does not have an active subscription. Sessions are read-only until the subscription is reactivated.",
        )
        return redirect("events:session_list", event_id=event.id)

    if request.method == "POST":
        session.delete()
        messages.success(request, "Session deleted successfully.")
        return redirect("events:session_list", event_id=event.id)

    return render(request, "events/session_confirm_delete.html", {"event": event, "session": session})


@login_required
@organiser_required
def event_registrations(request, event_id):
    """显示 organiser 可查看的 event registrations 和 session capacity。"""
    event = get_object_or_404(Event.objects.prefetch_related("sessions"), pk=event_id)

    # organiser 只能看自己 organisation event 的 registrations，避免查看其他 organiser 的 attendee 数据。
    if not can_manage_event(request.user, event):
        messages.error(request, "You can only view registrations for events in your own organisation.")
        return redirect("events:organiser_event_list")

    registrations = (
        Registration.objects.filter(event=event)
        .select_related("user")
        .prefetch_related("session_selections__session")
        .order_by("-created_at")
    )
    active_registration_count = get_event_registered_count(event)
    event_remaining_capacity = max(event.capacity - active_registration_count, 0)
    sessions = add_remaining_capacity_to_sessions(list(event.sessions.all().order_by("start_datetime")))

    context = {
        "event": event,
        "registrations": registrations,
        "active_registration_count": active_registration_count,
        "event_remaining_capacity": event_remaining_capacity,
        "event_is_full": event_remaining_capacity <= 0,
        "sessions": sessions,
    }
    return render(request, "events/event_registrations.html", context)


@login_required
def event_register(request, event_id):
    """已登录用户报名 published event，并选择 sessions。"""
    event = get_object_or_404(Event.objects.prefetch_related("sessions"), pk=event_id)
    role = get_user_role(request.user)

    if request.user.is_superuser or role == UserProfile.Role.ADMIN:
        messages.error(request, "Administrator accounts cannot register for events.")
        return redirect("events:event_detail", event_id=event.id)

    if event.status != Event.Status.PUBLISHED:
        messages.error(request, "Only published events are open for registration.")
        return redirect("events:event_detail", event_id=event.id)

    existing_registration = Registration.objects.filter(event=event, user=request.user).first()
    if existing_registration and existing_registration.status == Registration.Status.REGISTERED:
        # 防止同一个 attendee 重复报名同一个 event。
        messages.warning(request, "You have already registered for this event.")
        return redirect("events:my_registrations")

    # 检查 event capacity，避免 event 总报名人数超出容量。
    event_remaining_capacity = max(event.capacity - get_event_registered_count(event), 0)
    if event_remaining_capacity <= 0 and request.method == "POST":
        messages.error(request, "This event has reached its total registration capacity.")
        return redirect("events:event_detail", event_id=event.id)

    if request.method == "POST":
        form = EventRegistrationForm(request.POST, event=event)
        if form.is_valid():
            selected_sessions = form.cleaned_data["sessions"]
            with transaction.atomic():
                if existing_registration:
                    registration = existing_registration
                    registration.status = Registration.Status.REGISTERED
                    registration.save(update_fields=["status", "updated_at"])
                    registration.session_selections.all().delete()
                else:
                    registration = Registration.objects.create(
                        event=event,
                        user=request.user,
                        status=Registration.Status.REGISTERED,
                    )

                # SessionSelection 将 registration 和用户选择的 sessions 连接起来。
                for session in selected_sessions:
                    SessionSelection.objects.create(registration=registration, session=session)

            messages.success(request, "You have registered for this event.")
            return redirect("events:my_registrations")

        messages.error(request, "Registration failed. Please review the form.")
    else:
        form = None if event_remaining_capacity <= 0 else EventRegistrationForm(event=event)

    sessions = add_remaining_capacity_to_sessions(list(event.sessions.all().order_by("start_datetime")))
    context = {
        "event": event,
        "form": form,
        "event_remaining_capacity": event_remaining_capacity,
        "event_full": event_remaining_capacity <= 0,
        "event_sessions": sessions,
    }
    return render(request, "events/event_register.html", context)


@login_required
def my_registrations(request):
    """显示当前用户自己的报名记录。"""
    registrations = (
        Registration.objects.filter(user=request.user)
        .select_related("event")
        .prefetch_related("session_selections__session")
        .order_by("-created_at")
    )
    return render(request, "events/my_registrations.html", {"registrations": registrations})


@login_required
def registration_cancel(request, registration_id):
    """取消自己的 registration，不删除历史记录。"""
    registration = get_object_or_404(
        Registration.objects.select_related("event", "user"),
        pk=registration_id,
    )

    if registration.user != request.user:
        messages.error(request, "You can only cancel your own registrations.")
        return redirect("events:my_registrations")

    if request.method == "POST":
        registration.status = Registration.Status.CANCELLED
        registration.save(update_fields=["status", "updated_at"])
        messages.success(request, "Your registration has been cancelled.")
        return redirect("events:my_registrations")

    return render(request, "events/registration_confirm_cancel.html", {"registration": registration})
