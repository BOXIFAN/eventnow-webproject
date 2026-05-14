# EventNow

EventNow is a Django-based event management platform for the INFS3202/7202 Web Information Systems formal web project.

## Project Overview

EventNow supports event browsing, organiser event/session management, attendee registration with session selection, organiser registration tracking, subscription management, and a rule-based recommendation algorithm.

## Tech Stack

- Backend: Django
- Frontend: Django Templates
- Styling: CSS
- Database: SQLite
- Deployment helpers: WhiteNoise, python-dotenv, Pillow

## Current Project Structure

```text
eventnow/
  config/              # Django settings, URLs, WSGI/ASGI
  accounts/            # Authentication, UserProfile, role logic
  events/              # Events, sessions, registrations, recommendations
  subscriptions/       # Organisations and SaaS subscriptions
  templates/           # Shared and app templates
  static/css/          # Main stylesheet
  manage.py
  requirements.txt
  .env.example
```

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## How to Run Checks

```bash
python manage.py check
python manage.py makemigrations --dry-run --check
python manage.py collectstatic --noinput
```

## Demo Accounts

Create these accounts locally before demonstration:

- Superuser/admin: create with `python manage.py createsuperuser`
- Attendee: register through `/accounts/register/`
- Organiser: register a normal user, then use Django Admin to update `UserProfile.role` to `organiser`

For organiser event creation, ensure the organiser owns an active `Organisation` with an active current `Subscription`.

## Deployment URL

Deployment URL placeholder:

```text
TBA
```

## UQ Cloud Zone Deployment

The project can be deployed to a UQ Cloud Zone `webproject` using the `uwsgi312` environment.

Recommended project path on the server:

```text
/var/www/uwsgi/eventnow
```

### 1. Upload project

Upload the repository contents to:

```text
/var/www/uwsgi/eventnow
```

### 2. Create and activate virtual environment

Use either Python 3.12 explicitly or the default Python 3 command available in the zone:

```bash
cd /var/www/uwsgi/eventnow
python3.12 -m venv env
source env/bin/activate
```

If `python3.12` is not available as a direct command:

```bash
cd /var/www/uwsgi/eventnow
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the environment file

Create `.env` in `/var/www/uwsgi/eventnow` using `.env.example` as a template:

```bash
cp .env.example .env
```

Example production values:

```env
SECRET_KEY=replace-this-with-a-production-secret
DEBUG=False
ALLOWED_HOSTS=your-zone-hostname,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://your-zone-hostname
DATABASE_URL=
```

### 5. Run Django setup commands

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py seed_demo_data
```

### 6. Sample `uwsgi.ini`

Configure `/etc/uwsgi/uwsgi.ini` with a block similar to:

```ini
[uwsgi]
module = config.wsgi:application
chdir = /var/www/uwsgi/eventnow
virtualenv = /var/www/uwsgi/eventnow/env
env = DJANGO_SETTINGS_MODULE=config.settings
workers = 2
```

### 7. nginx static/media aliases

Add aliases for collected static files and uploaded media:

```nginx
location /static/ {
    alias /var/www/uwsgi/eventnow/staticfiles/;
}

location /media/ {
    alias /var/www/uwsgi/eventnow/media/;
}
```

### 8. Restart services

After config changes:

```bash
systemctl restart uwsgi
systemctl reload nginx
```

### 9. Deployment checklist

Before final verification, confirm:

- `.env` exists and production values are set
- `DEBUG=False`
- `ALLOWED_HOSTS` includes the zone hostname
- `CSRF_TRUSTED_ORIGINS` includes the zone origin
- `python manage.py migrate` completed successfully
- `python manage.py collectstatic --noinput` completed successfully
- nginx aliases point to `staticfiles/` and `media/`

## Implemented Features Mapped to Rubric

- Authentication and authorization: login/register/logout, `UserProfile`, role-based decorators
- Event website: public event list/detail with sessions
- Organiser event management: create/edit/archive events
- Session management: create/edit/delete sessions under events
- Registration workflow: attendee event registration and session selection
- Tracking: organiser registration list and session capacity dashboard
- Admin subscription interface: custom list/create/edit/archive pages with paging/search/filter
- Archive behavior: subscriptions/events are archived rather than hard-deleted where required
- Advanced feature: transparent rule-based event recommendation algorithm

## Recommendation Algorithm

The recommendation algorithm is implemented in `events/recommendations.py`.

It recommends only published events with available event capacity and at least one available session. It excludes events the user has already registered for, as well as draft, pending, archived, full, or no-session events.

Scoring:

- Similar category: +5
- Same organiser organisation: +3
- Event has remaining capacity: +2
- At least one session has remaining capacity: +2
- Event starts within the next 14 days: +1

The algorithm is rule-based and explainable. It does not use an external AI API or chatbot.

## Security and Role Authorization

- New users register as attendees by default.
- Organiser access must be approved by admin/superuser through `UserProfile`.
- Organisers can only manage their own events.
- Organisers require an active organisation subscription to create or modify events/sessions.
- Expired or archived subscriptions put organisers into read-only mode.
- Admin/superuser can manage all events, sessions, and subscriptions.
- Public users only see published events.
- Archived events remain available to owner organiser/admin/superuser records, but are hidden from public users.

## Testing

Use [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) for role-based manual testing.

Recommended checks:

```bash
python manage.py check
python manage.py seed_demo_data
python manage.py runserver
```

For UQ Cloud Zone deployment validation, also run:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## Code Review Preparation

Use [CODE_REVIEW_NOTES.md](CODE_REVIEW_NOTES.md) to explain feature-to-file mapping, data flow, permissions, and the recommendation algorithm.

## GenAI Usage Declaration

Codex / ChatGPT was used to assist with planning, code drafting, debugging, documentation, and explanation.

I reviewed and tested the generated code. I am responsible for the final implementation and can explain how the code works.
