"""subscriptions app 的 URL routing。"""
from django.urls import path

from . import views


app_name = "subscriptions"

urlpatterns = [
    path("", views.subscription_list, name="subscription_list"),
    path("request-access/", views.organisation_request, name="organisation_request"),
    path("create/", views.subscription_create, name="subscription_create"),
    path("<int:subscription_id>/edit/", views.subscription_edit, name="subscription_edit"),
    path("<int:subscription_id>/archive/", views.subscription_archive, name="subscription_archive"),
    path("<int:subscription_id>/reactivate/", views.subscription_reactivate, name="subscription_reactivate"),
    path("organisations/<int:organisation_id>/reject/", views.organisation_reject, name="organisation_reject"),
]
