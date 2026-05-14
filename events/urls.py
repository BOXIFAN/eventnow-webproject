"""events app 的 URL routing。"""
from django.urls import path

from . import views


app_name = "events"

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("recommended/", views.recommended_events, name="recommended_events"),
    path("my-registrations/", views.my_registrations, name="my_registrations"),
    path("organiser/dashboard/", views.organiser_dashboard, name="organiser_dashboard"),
    path("organiser/events/", views.organiser_event_list, name="organiser_event_list"),
    path("organiser/events/create/", views.event_create, name="event_create"),
    path("organiser/events/<int:event_id>/edit/", views.event_edit, name="event_edit"),
    path("organiser/events/<int:event_id>/archive/", views.event_archive, name="event_archive"),
    path("organiser/events/<int:event_id>/registrations/", views.event_registrations, name="event_registrations"),
    path("organiser/events/<int:event_id>/sessions/", views.session_list, name="session_list"),
    path("organiser/events/<int:event_id>/sessions/create/", views.session_create, name="session_create"),
    path("organiser/sessions/<int:session_id>/edit/", views.session_edit, name="session_edit"),
    path("organiser/sessions/<int:session_id>/delete/", views.session_delete, name="session_delete"),
    path("registrations/<int:registration_id>/cancel/", views.registration_cancel, name="registration_cancel"),
    path("<int:event_id>/register/", views.event_register, name="event_register"),
    path("<int:event_id>/", views.event_detail, name="event_detail"),
]
