# EventNow Code Review Notes

Use this document to prepare for Project Demonstration & Code Review.

## 1. Authentication and UserProfile

- Files involved:
  - `accounts/models.py`
  - `accounts/forms.py`
  - `accounts/views.py`
  - `accounts/urls.py`
  - `templates/accounts/login.html`
  - `templates/accounts/register.html`

- What the feature does:
  - Uses Django's built-in `User`.
  - Extends user role information through `UserProfile`.
  - New users register as attendee by default.
  - Organiser/admin roles must be assigned by platform admin.

- Data flow:
  - `RegisterForm` creates `User`.
  - `RegisterForm.save()` creates `UserProfile(role='attendee')`.
  - `login_view` uses `AuthenticationForm`.
  - `dashboard_redirect_view` redirects based on role.

- Code review explanation:
  - Explain why the project does not use a custom User model.
  - Explain why organiser access requires admin approval.

## 2. Role Authorization Decorators

- Files involved:
  - `accounts/decorators.py`
  - `events/views.py`
  - `subscriptions/views.py`

- What the feature does:
  - `get_user_role()` safely reads `user.userprofile.role`.
  - `organiser_required` protects organiser workflows.
  - `admin_required` protects subscription management.

- Data flow:
  - Request enters view.
  - `login_required` checks authentication.
  - Custom decorator checks role.
  - Unauthorized users receive message and redirect.

- Code review explanation:
  - Explain how missing `UserProfile` is handled safely.
  - Explain why superuser is treated as high-level admin.

## 3. Subscription Management

- Files involved:
  - `subscriptions/models.py`
  - `subscriptions/forms.py`
  - `subscriptions/views.py`
  - `subscriptions/urls.py`
  - `templates/subscriptions/*.html`

- What the feature does:
  - Models organiser organisations and SaaS subscriptions.
  - Supports list/create/edit/archive subscription workflow.
  - Supports paging, search, and status filter.
  - Archive marks status instead of deleting records.

- Data flow:
  - `Organisation` owns events through organiser.
  - `Subscription` belongs to an organisation.
  - `SubscriptionForm` validates date range.
  - `subscription_list` filters and paginates subscriptions.
  - `subscription_archive` sets status to archived.

- Code review explanation:
  - Explain `Organisation.has_active_subscription()`.
  - Explain why archive is used instead of delete.
  - Explain how inactive subscription limits organiser write access.

## 4. Event CRUD

- Files involved:
  - `events/models.py`
  - `events/forms.py`
  - `events/views.py`
  - `events/urls.py`
  - `templates/events/organiser_event_list.html`
  - `templates/events/event_form.html`
  - `templates/events/event_confirm_archive.html`

- What the feature does:
  - Organisers create, edit, and archive their own events.
  - Admin/superuser can manage all events.
  - Public event list only shows published events.
  - Organiser-created events require admin approval before public display.

- Data flow:
  - `EventForm` validates event data and limits status choices.
  - `event_create` sets `organiser=request.user`.
  - `event_edit` and `event_archive` check ownership/write access.
  - `event_list` filters to published events.

- Code review explanation:
  - Explain organiser ownership protection.
  - Explain status workflow: draft, pending, published, archived.
  - Explain subscription write access checks.

## 5. Session CRUD

- Files involved:
  - `events/models.py`
  - `events/forms.py`
  - `events/views.py`
  - `templates/events/session_list.html`
  - `templates/events/session_form.html`
  - `templates/events/session_confirm_delete.html`

- What the feature does:
  - Organisers manage sessions under their own events.
  - Session belongs to event from URL, not from form input.
  - Session capacity is validated against event capacity.

- Data flow:
  - `SessionForm` validates time and capacity.
  - `session_create` assigns `session.event`.
  - `session_edit/delete` use the parent event for permission checks.

- Code review explanation:
  - Explain why event is not selectable in `SessionForm`.
  - Explain why inactive subscription makes sessions read-only.

## 6. Registration and SessionSelection

- Files involved:
  - `events/models.py`
  - `events/forms.py`
  - `events/views.py`
  - `templates/events/event_register.html`
  - `templates/events/my_registrations.html`
  - `templates/events/registration_confirm_cancel.html`

- What the feature does:
  - Attendees register for published events.
  - Attendees select one or more sessions.
  - Users cannot register twice for the same active event.
  - Cancelled registrations remain as records.

- Data flow:
  - `EventRegistrationForm` dynamically lists event sessions.
  - `event_register` creates `Registration`.
  - Selected sessions create `SessionSelection` rows.
  - `registration_cancel` changes status to cancelled.

- Code review explanation:
  - Explain unique constraints on registration/session selection.
  - Explain why cancelled records are not deleted.

## 7. Capacity Tracking

- Files involved:
  - `events/views.py`
  - `events/forms.py`
  - `templates/events/event_detail.html`
  - `templates/events/event_registrations.html`

- What the feature does:
  - Tracks event total registration capacity.
  - Tracks session selection capacity.
  - Excludes cancelled registrations from active capacity.
  - Shows organiser capacity dashboards.

- Data flow:
  - Count active `Registration(status='registered')`.
  - Count active `SessionSelection` through registered registrations.
  - Views attach remaining capacity values for templates.

- Code review explanation:
  - Explain event capacity vs session capacity.
  - Explain why cancelled registrations are excluded.

## 8. Recommendation Algorithm

- Files involved:
  - `events/recommendations.py`
  - `events/views.py`
  - `templates/events/recommended_events.html`

- What the feature does:
  - Recommends published events with available capacity.
  - Excludes already registered, full, non-published, or no-session events.
  - Uses rule-based scoring, not external AI.

- Data flow:
  - User registration history creates category/organisation preferences.
  - `get_recommended_events()` scores candidate events.
  - `recommended_events` view sends score and reasons to template.

- Code review explanation:
  - Explain scoring rules:
    - category match +5
    - organisation match +3
    - event capacity +2
    - session capacity +2
    - starts within 14 days +1
  - Explain why this is transparent and suitable for review.

## 9. UI Templates and Static Files

- Files involved:
  - `templates/base.html`
  - `static/css/main.css`
  - `templates/events/*.html`
  - `templates/subscriptions/*.html`
  - `templates/accounts/*.html`

- What the feature does:
  - Provides shared layout, navigation, messages, and responsive styling.
  - Shows role-specific navigation.
  - Uses consistent cards, tables, badges, forms, and buttons.

- Data flow:
  - Views pass context.
  - Templates display data and role-specific actions.
  - CSS provides consistent responsive presentation.

- Code review explanation:
  - Explain how `base.html` centralizes navigation and messages.
  - Explain how templates hide unavailable actions for read-only states.
