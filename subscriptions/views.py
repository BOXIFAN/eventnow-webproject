"""subscriptions app 的页面视图。"""
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import admin_required
from accounts.models import UserProfile

from .forms import OrganisationRequestForm, SubscriptionForm
from .models import Organisation, Subscription


def promote_owner_to_organiser(organisation):
    """当 organisation 被激活时，确保 owner 拥有 organiser role。"""
    profile, _ = UserProfile.objects.get_or_create(user=organisation.owner)
    if profile.role != UserProfile.Role.ADMIN:
        profile.role = UserProfile.Role.ORGANISER
        profile.save(update_fields=["role", "updated_at"])


def get_user_request_state(user):
    """返回当前用户的 organiser access request 状态。"""
    organisations = user.organisations.exclude(status=Organisation.Status.ARCHIVED).order_by("-created_at")
    active_organisation = organisations.filter(status=Organisation.Status.ACTIVE).first()
    pending_organisation = organisations.filter(status=Organisation.Status.PENDING).first()
    rejected_organisation = organisations.filter(status=Organisation.Status.REJECTED).first()
    return {
        "active_organisation": active_organisation,
        "pending_organisation": pending_organisation,
        "rejected_organisation": rejected_organisation,
        "has_requestable_gap": not active_organisation and not pending_organisation,
    }


@login_required
@admin_required
def subscription_list(request):
    """显示 subscription 管理列表。

    只有 admin/superuser 可以管理 subscriptions；分页每页显示 10 条。
    """
    subscriptions = Subscription.objects.select_related("organisation", "organisation__owner")
    pending_organisations = Organisation.objects.filter(status=Organisation.Status.PENDING).select_related("owner")

    keyword = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()

    if keyword:
        subscriptions = subscriptions.filter(
            Q(organisation__name__icontains=keyword) | Q(plan_name__icontains=keyword)
        )

    if status:
        subscriptions = subscriptions.filter(status=status)

    subscriptions = subscriptions.order_by("-start_date", "organisation__name")
    paginator = Paginator(subscriptions, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "subscriptions": page_obj.object_list,
        "pending_organisations": pending_organisations.order_by("created_at", "name"),
        "keyword": keyword,
        "status": status,
        "status_choices": Subscription.Status.choices,
    }
    return render(request, "subscriptions/subscription_list.html", context)


@login_required
@admin_required
def subscription_create(request):
    """创建 subscription。"""
    organisation_id = request.GET.get("organisation", "").strip()

    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save()
            organisation = subscription.organisation
            if organisation.status != Organisation.Status.ACTIVE:
                organisation.status = Organisation.Status.ACTIVE
                organisation.save(update_fields=["status", "updated_at"])
            promote_owner_to_organiser(organisation)
            messages.success(request, "Subscription created successfully.")
            return redirect("subscriptions:subscription_list")

        messages.error(request, "Subscription creation failed. Please review the form.")
    else:
        initial = {"organisation": organisation_id} if organisation_id else None
        form = SubscriptionForm(initial=initial)

    return render(
        request,
        "subscriptions/subscription_form.html",
        {"form": form, "page_title": "Create Subscription", "submit_label": "Save Subscription"},
    )


@login_required
@admin_required
def subscription_edit(request, subscription_id):
    """编辑 subscription。"""
    subscription = get_object_or_404(Subscription, pk=subscription_id)

    if request.method == "POST":
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            updated_subscription = form.save()
            if updated_subscription.status == Subscription.Status.ACTIVE:
                organisation = updated_subscription.organisation
                if organisation.status != Organisation.Status.ACTIVE:
                    organisation.status = Organisation.Status.ACTIVE
                    organisation.save(update_fields=["status", "updated_at"])
                promote_owner_to_organiser(organisation)
            messages.success(request, "Subscription updated successfully.")
            return redirect("subscriptions:subscription_list")

        messages.error(request, "Subscription update failed. Please review the form.")
    else:
        form = SubscriptionForm(instance=subscription)

    return render(
        request,
        "subscriptions/subscription_form.html",
        {
            "form": form,
            "subscription": subscription,
            "page_title": "Edit Subscription",
            "submit_label": "Save Changes",
        },
    )


@login_required
@admin_required
def subscription_archive(request, subscription_id):
    """archive subscription，不真正删除数据库记录。"""
    subscription = get_object_or_404(Subscription, pk=subscription_id)

    if request.method == "POST":
        # archive 代替 delete，保留历史订阅记录供 admin 审计和 demo 展示。
        subscription.status = Subscription.Status.ARCHIVED
        subscription.save(update_fields=["status", "updated_at"])
        messages.success(request, "Subscription archived successfully.")
        return redirect("subscriptions:subscription_list")

    return render(
        request,
        "subscriptions/subscription_confirm_archive.html",
        {"subscription": subscription},
    )


@login_required
def organisation_request(request):
    """普通用户申请 organiser publishing access。"""
    request_state = get_user_request_state(request.user)

    if request_state["active_organisation"]:
        messages.info(request, "You already have an organisation record. Please contact the administrator for subscription changes.")
        return redirect("events:event_list")

    if request_state["pending_organisation"] and request.method != "POST":
        form = None
    elif request.method == "POST":
        if not request_state["has_requestable_gap"]:
            messages.warning(request, "You already have a pending or active organisation request.")
            return redirect("subscriptions:organisation_request")

        form = OrganisationRequestForm(request.POST)
        if form.is_valid():
            organisation = form.save(commit=False)
            organisation.owner = request.user
            organisation.status = Organisation.Status.PENDING
            organisation.save()
            messages.success(request, "Your organiser access request has been submitted for admin review.")
            return redirect("subscriptions:organisation_request")

        messages.error(request, "Organisation request failed. Please review the form.")
    else:
        form = OrganisationRequestForm()

    context = {
        "form": form,
        "request_state": get_user_request_state(request.user),
    }
    return render(request, "subscriptions/organisation_request_form.html", context)


@login_required
@admin_required
def organisation_reject(request, organisation_id):
    """拒绝 pending organisation request。"""
    organisation = get_object_or_404(Organisation, pk=organisation_id)

    if request.method == "POST":
        organisation.status = Organisation.Status.REJECTED
        organisation.save(update_fields=["status", "updated_at"])
        messages.success(request, f"{organisation.name} has been marked as rejected.")
        return redirect("subscriptions:subscription_list")

    return redirect("subscriptions:subscription_list")


@login_required
@admin_required
def subscription_reactivate(request, subscription_id):
    """重新激活 archived/expired subscription。"""
    subscription = get_object_or_404(Subscription.objects.select_related("organisation", "organisation__owner"), pk=subscription_id)

    if request.method == "POST":
        today = timezone.localdate()
        subscription.status = Subscription.Status.ACTIVE
        subscription.start_date = today
        subscription.end_date = today + timedelta(days=365)
        subscription.save(update_fields=["status", "start_date", "end_date", "updated_at"])

        organisation = subscription.organisation
        if organisation.status != Organisation.Status.ACTIVE:
            organisation.status = Organisation.Status.ACTIVE
            organisation.save(update_fields=["status", "updated_at"])
        promote_owner_to_organiser(organisation)

        messages.success(request, "Subscription reactivated successfully.")
        return redirect("subscriptions:subscription_list")

    return redirect("subscriptions:subscription_list")
