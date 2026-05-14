# EventNow

## Deployment URL

Production deployment:

```text
https://s4752211-s4752211-eventnow.uqcloud.net
```

## Demo Login Accounts

The same account information is also provided in [LOGIN_DETAILS.md](LOGIN_DETAILS.md) for quick reference during marking.

| Account | Username | Password | Intended use |
|---|---|---|---|
| Primary marker/admin account | `superadmin` | `1403` | Main platform administrator account for marking. Use this account to access the custom subscription management workflow and platform-level admin features. |
| Superuser | `superuser` | `82221789dd` | Site-level superuser account for ordinary event-related actions. It should not be treated as the primary admin account, and it is not the account intended for Django admin editing in this submission. |
| Organiser | `organiser` | `82221789dd` | Organiser workflow account. It can request/hold organisation access and publish/manage events when permitted by organisation ownership and subscription status. |
| Attendee | `attendee` | `82221789dd` | Attendee workflow account for browsing events, registering for events/sessions, viewing registrations, and using recommendation features. |

## Project Overview

EventNow is the INFS3202/7202 Web Information Systems final web project. It is a Django-based event management platform for campus and local events.

The system supports:

- public landing page and event browsing
- password-based registration, login, and logout
- attendee event registration with session selection
- organiser event and session management
- organiser access controlled by organisation ownership and active subscription status
- subscription administration for SaaS-style organiser publishing access
- a rule-based event recommendation algorithm

## Implemented Features Mapped to Rubric

| Rubric area | Implemented evidence in this project | Where/how to test |
|---|---|---|
| Project deployment to server and login accounts provided | Live deployment on UQ Cloud Zone and demo accounts included in this README and `LOGIN_DETAILS.md` | Open the deployment URL and log in with the accounts above |
| Landing page and password-based login | Public landing page, register page, login page, logout flow | Visit `/`, `/accounts/register/`, `/accounts/login/` |
| Role authorization across web pages and features | `UserProfile` role model plus organiser/admin checks across pages and view logic | Compare attendee, organiser, and `superadmin` access to organiser/subscription pages |
| Admin interface for SaaS subscriptions | Custom subscription management with create/list/edit/archive/reactivate, pending organisation handling, and paging/filtering | Log in as `superadmin`, open `/subscriptions/` |
| UI for events | Event browse/list/detail, organiser create/edit/archive, ownership restrictions | Test `/events/`, event detail, organiser dashboard, manage events |
| UI for event sessions | Session create/list/edit/delete under organiser event workflow | Log in as organiser/admin and open Manage Sessions from an event |
| Arrange and schedule event sessions | Sessions are created under events with start/end times and capacity validation | Create/edit sessions from organiser event workflow |
| Display event website with sessions and process registration forms | Event detail page shows sessions, capacity, images where available, and attendee registration entry | Open a published event detail and register |
| Track registrations and show session capacity | Registration tracking page, event remaining capacity, session remaining capacity | Use organiser registration tracking and event/session detail pages |
| UI/UX quality | Themed landing page, consistent buttons/cards/forms, responsive layouts, mobile table cards, accessibility-focused labels and focus styles | Review on desktop and mobile widths, especially around 390–450px |
| Advanced feature | Rule-based recommendation algorithm based on prior registrations, category/organisation affinity, capacity, and timing | Log in as attendee and open `/events/recommended/` |

## User Roles and Permissions

### Attendee

- Can register and log in with password-based authentication.
- Can browse published events.
- Can view event details and sessions.
- Can register for public events and selected sessions.
- Can view and cancel their own registrations.
- Can access recommended events.

### Organiser

- Uses the organiser dashboard and organiser event workflow.
- Can request organiser/organisation access if they do not yet have an approved organisation.
- Can only manage events that belong to their own organisation.
- Requires an active subscription to create events, edit/archive events, and create/edit/delete sessions.
- If subscription access is inactive, organiser records remain visible in read-only mode.
- Can still browse and register for public events as a normal user.

### Admin / Super Admin

- `superadmin` is the primary marker/admin account for platform-level testing.
- Can manage all events, sessions, and subscriptions.
- Can review pending organisations and create active subscriptions.
- Can archive and reactivate subscriptions.
- Can publish/review organiser content as needed.

## Main Testing Workflow for Marker

Suggested order for marking:

1. Open the deployment URL and confirm the landing page loads.
2. Log in with `attendee` and test event browsing, event registration, My Registrations, and Recommended Events.
3. Log in with `organiser` and test Organiser Dashboard, Manage Events, event create/edit/archive, session create/list/edit/delete, and registration tracking.
4. If organiser publishing access is inactive, confirm organiser pages become read-only while public event registration still works.
5. Log in with `superadmin` and test Subscription Management, pending organisation handling, create/edit/archive/reactivate subscription, and platform-level event management.
6. Check mobile responsiveness around 390–450px, especially navigation, public cards, and management page responsive table/card layouts.

For a fuller checklist, see [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md).

## Technology Stack

- Backend: Django
- Frontend: Django Templates + CSS
- Database: SQLite
- Authentication: Django built-in auth with password login
- Static/media helpers: WhiteNoise, Pillow
- Configuration helpers: python-dotenv
- Deployment target: UQ Cloud Zone with uWSGI + nginx

## Local Setup Instructions

```bash
python -m venv env
source env/bin/activate
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

Useful checks:

```bash
python manage.py check
python manage.py makemigrations --dry-run --check
```

## Deployment Notes for UQ Cloud Zone

EventNow is deployed on UQ Cloud Zone using uWSGI and nginx.

Recommended server project path:

```text
/var/www/uwsgi/eventnow
```

Typical setup steps:

```bash
cd /var/www/uwsgi/eventnow
python3.12 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py seed_demo_data
```

Sample `uwsgi.ini`:

```ini
[uwsgi]
module = config.wsgi:application
chdir = /var/www/uwsgi/eventnow
virtualenv = /var/www/uwsgi/eventnow/env
env = DJANGO_SETTINGS_MODULE=config.settings
workers = 2
```

nginx static/media snippet:

```nginx
location /static/ {
    alias /var/www/uwsgi/eventnow/staticfiles/;
}

location /media/ {
    alias /var/www/uwsgi/eventnow/media/;
}
```

After deployment changes:

```bash
systemctl restart uwsgi
systemctl reload nginx
```

Notes:

- static files are collected with `collectstatic`
- uploaded event images are stored under `media/`
- uploaded media is served through the nginx media alias
- the server `.env` file is not included in GitHub or submission materials

## Recommendation Algorithm Explanation

The recommendation feature is implemented in `events/recommendations.py`.

It is a transparent rule-based scoring approach rather than an AI chatbot feature. The system recommends only published events that:

- are not already registered by the current user
- still have remaining event capacity
- have at least one session with remaining capacity

Scoring currently uses:

- Similar category: `+5`
- Same organiser organisation: `+3`
- Available event capacity: `+2`
- Available session capacity: `+2`
- Starts within the next 14 days: `+1`

If a user has no registration history, the system falls back to recommending available upcoming events.

## Accessibility and UI/UX Notes

The interface was designed to support a professional and marker-friendly workflow:

- consistent purple/white themed visual design across public and management pages
- clear navigation for attendee, organiser, and admin flows
- visible form labels and readable status badges
- clear button hierarchy for primary, secondary, danger, and disabled actions
- focus-visible states for keyboard accessibility
- responsive layouts for public cards, forms, and management pages
- mobile-friendly management table/card layouts around 390–450px
- event images displayed with fixed-size responsive containers to avoid layout breakage

## Security Notes

This project includes practical role-based protections relevant to the assignment:

- password-based authentication using Django auth
- role-based page and feature restrictions
- organiser ownership checks for event/session/registration management
- subscription-based publishing restrictions for organiser write actions
- read-only behaviour when organiser subscription access is inactive
- public event pages show only published events
- environment-variable-based deployment settings for secret key, debug, allowed hosts, and CSRF trusted origins

This project does not claim perfect production security. It is a course project with reasonable access control and deployment precautions for the assignment scope.

## Use of Generative AI Declaration

Generative AI tools including ChatGPT/Codex were used to support debugging, deployment troubleshooting, README/checklist drafting, and frontend refinement suggestions. The final implementation was reviewed, tested, and adapted by me, and I am responsible for explaining the code in the demonstration/code review.

## Known Limitations

- The project uses SQLite as its current database configuration.
- Public pages do not include social login or external identity providers.
- Event categories and venues are maintained through Django admin/reference-data workflows rather than a separate custom front-end CRUD interface.
- Uploaded event images are supported, but advanced image processing/cropping is not implemented.
- The recommendation system is rule-based and explainable, but not personalised with machine learning.
