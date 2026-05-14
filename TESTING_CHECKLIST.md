# EventNow Testing Checklist

Use this checklist before submission and demonstration. Fill in `Actual Result`, `Pass/Fail`, and `Notes` while testing.

## A. Visitor / 未登录用户测试

| Test ID | Role | Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|---|
| A01 | Visitor | Landing page is accessible | Open `/` | Home page loads with header, navigation, content, footer |  |  |  |
| A02 | Visitor | Published events can be browsed | Open `/events/` | Only published events are listed |  |  |  |
| A03 | Visitor | Draft/pending/archived events are hidden | Compare public list with admin/organiser events | Non-published events do not appear publicly |  |  |  |
| A04 | Visitor | Event detail visibility | Open a published event detail URL | Published event detail is visible |  |  |  |
| A05 | Visitor | Non-public event detail is blocked | Open draft/pending/archived event detail URL | Error message and redirect to event list |  |  |  |
| A06 | Visitor | Register requires login | Click Register for Event | Redirects to login page |  |  |  |
| A07 | Visitor | Organiser dashboard blocked | Open `/events/organiser/dashboard/` | Redirects to login |  |  |  |
| A08 | Visitor | Subscriptions blocked | Open `/subscriptions/` | Redirects to login |  |  |  |
| A09 | Visitor | Management pages blocked | Open manage events/sessions/registrations URLs | Redirects to login |  |  |  |

## B. Attendee 测试

| Test ID | Role | Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|---|
| B01 | Attendee | Register account | Register through `/accounts/register/` | Account is created successfully |  |  |  |
| B02 | Attendee | Default role | Check UserProfile in Django Admin | New user role is attendee |  |  |  |
| B03 | Attendee | Login/logout | Login then logout | Correct messages and redirects |  |  |  |
| B04 | Attendee | Browse published events | Open `/events/` | Published events are visible |  |  |  |
| B05 | Attendee | Register event | Open published event detail and register | Registration succeeds |  |  |  |
| B06 | Attendee | Select sessions | Choose sessions during registration | SessionSelection records are created |  |  |  |
| B07 | Attendee | Duplicate registration blocked | Try registering same event again | Warning shown; duplicate blocked |  |  |  |
| B08 | Attendee | Event full blocked | Fill event capacity then register | Registration blocked |  |  |  |
| B09 | Attendee | Session full blocked | Fill session capacity then select session | Full session cannot be selected |  |  |  |
| B10 | Attendee | My Registrations | Open `/events/my-registrations/` | User registrations and sessions are listed |  |  |  |
| B11 | Attendee | Cancel registration | Cancel an active registration | Status becomes cancelled, record remains |  |  |  |
| B12 | Attendee | Cancelled not counted | Check event/session capacity after cancel | Cancelled registration does not count as active capacity |  |  |  |
| B13 | Attendee | Recommended Events access | Open `/events/recommended/` | Recommendation page loads |  |  |  |
| B14 | Attendee | Registered events excluded | Register for an event then view recommendations | Registered event is not recommended |  |  |  |
| B15 | Attendee | Non-public/full events excluded | Check recommendation results | Draft/pending/archived/full events are not recommended |  |  |  |
| B16 | Attendee | Request organiser access | Open `/subscriptions/request-access/` and submit organisation request | Pending organisation is created and success message shows |  |  |  |

## C. Organiser with Active Subscription 测试

| Test ID | Role | Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|---|
| C01 | Organiser | Login | Login as approved organiser | Login succeeds |  |  |  |
| C02 | Organiser | Dashboard access | Open `/events/organiser/dashboard/` | Dashboard loads |  |  |  |
| C03 | Organiser | Dashboard stats | Review stat cards | Events, registrations, sessions, full sessions show |  |  |  |
| C04 | Organiser | Create event | Open create event page | Form is available |  |  |  |
| C05 | Organiser | Organisation restriction | Check organisation dropdown | Only active subscribed organisations owned by organiser appear |  |  |  |
| C06 | Organiser | Status restriction | Check status dropdown | Only draft/pending available |  |  |  |
| C07 | Organiser | Edit own event | Edit own event | Update succeeds |  |  |  |
| C08 | Organiser | Archive own event | Archive own event | Status becomes archived |  |  |  |
| C09 | Organiser | Archived public visibility | Open public event list | Archived event is hidden |  |  |  |
| C10 | Organiser | Manage sessions | Open Manage Sessions | Session list loads |  |  |  |
| C11 | Organiser | Create/edit/delete sessions | Use session CRUD | Operations succeed |  |  |  |
| C12 | Organiser | Session capacity validation | Set session capacity above event capacity | Validation error shown |  |  |  |
| C13 | Organiser | View registrations | Open View Registrations | Registration list and capacity overview show |  |  |  |
| C14 | Organiser | Ownership protection | Try managing another organiser event | Access denied and redirected |  |  |  |
| C15 | Organiser | Public attendee ability retained | Open a published event and register | Organiser can still register for public events when capacity is available |  |  |  |

## D. Organiser without Active Subscription / Archived Subscription 测试

| Test ID | Role | Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|---|
| D01 | Organiser | Login still works | Login with inactive subscription | Login succeeds |  |  |  |
| D02 | Organiser | Dashboard still works | Open organiser dashboard | Dashboard loads with warning |  |  |  |
| D03 | Organiser | View historical events | Open manage events | Events visible |  |  |  |
| D04 | Organiser | View event detail | Open own event detail | Detail visible |  |  |  |
| D05 | Organiser | View registrations | Open registrations page | Read-only registration data visible |  |  |  |
| D06 | Organiser | Create event blocked | Open/create event | Warning shown; save unavailable or blocked |  |  |  |
| D07 | Organiser | Edit event blocked | Try editing event | Error message; no edit allowed |  |  |  |
| D08 | Organiser | Archive event blocked | Try archiving event | Error message; archive blocked |  |  |  |
| D09 | Organiser | Session writes blocked | Try create/edit/delete session | Error message; write blocked |  |  |  |
| D10 | Organiser | Read-only UI | Check buttons | Write buttons hidden and read-only warning shown |  |  |  |
| D11 | Organiser | Public attendee ability retained | Register for a published event | Inactive subscription does not block public event registration |  |  |  |

## E. Admin / Superuser 测试

| Test ID | Role | Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|---|
| E01 | Admin | Access subscriptions | Open `/subscriptions/` | Subscription list loads |  |  |  |
| E02 | Admin | Create subscription | Use Create Subscription | Subscription created |  |  |  |
| E03 | Admin | List subscriptions | Review table | Subscriptions display with status badges |  |  |  |
| E04 | Admin | Edit subscription | Edit subscription | Changes saved |  |  |  |
| E05 | Admin | Archive subscription | Archive subscription | Status changes to archived; record remains |  |  |  |
| E06 | Admin | Paging/search/filter | Use page/search/status filter | Results update correctly |  |  |  |
| E07 | Admin | View all organiser events | Open organiser event list | All events visible |  |  |  |
| E08 | Admin | Edit event status | Edit pending event | Status can be set to published |  |  |  |
| E09 | Admin | Publish event | Set pending to published | Event appears publicly |  |  |  |
| E10 | Admin | Manage inactive organisation events | Edit/manage sessions for inactive subscription event | Admin is not blocked |  |  |  |
| E11 | Admin | See pending organisations | Open Subscription Management | Pending organisations section is visible |  |  |  |
| E12 | Admin | Activate pending organisation through subscription | Create active subscription for pending organisation | Organisation becomes active and owner becomes organiser |  |  |  |
| E13 | Admin | Reject pending organisation | Reject an organisation request | Organisation status becomes rejected |  |  |  |
| E14 | Admin | Reactivate subscription | Reactivate archived/expired subscription | Subscription becomes active and organiser publishing access returns |  |  |  |

## F. UI / Responsive / Accessibility 测试

| Test ID | Role | Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|---|
| F01 | All | Header/footer | Visit key pages | Header and footer appear consistently |  |  |  |
| F02 | All | Navigation clarity | Review navbar by role | Correct links shown for each role |  |  |  |
| F03 | All | Messages | Trigger success/error/warning | Messages are visible and readable |  |  |  |
| F04 | All | Mobile width | Test around 450px width | Content remains readable |  |  |  |
| F05 | All | Tables on small screen | View tables on mobile | Tables scroll or remain usable |  |  |  |
| F06 | All | Button labels | Review buttons | Labels are clear and action-oriented |  |  |  |
| F07 | All | Form labels | Review forms | Fields have labels |  |  |  |
| F08 | All | Error messages | Submit invalid forms | Errors are clear |  |  |  |
| F09 | All | Status badges | Review statuses | draft/pending/published/archived/full/read-only are visually clear |  |  |  |
| F10 | All | Consistent style | Browse workflows | Layout and styling are consistent |  |  |  |

## G. Deployment 测试

| Test ID | Role | Test Case | Steps | Expected Result | Actual Result | Pass/Fail | Notes |
|---|---|---|---|---|---|---|---|
| G01 | Developer | Local server | Run `python manage.py runserver` | Site opens locally |  |  |  |
| G02 | Developer | Collect static | Run `python manage.py collectstatic` | Static files collect successfully |  |  |  |
| G03 | Developer | DEBUG config | Set DEBUG through environment | App can be configured for production |  |  |  |
| G04 | Developer | Env docs | Review `.env.example` | Required variables documented |  |  |  |
| G05 | Developer | UQ Cloud Zone migration | Run `python manage.py migrate` on the zone | Database tables are created successfully |  |  |  |
| G06 | Developer | UQ Cloud Zone static collection | Run `python manage.py collectstatic --noinput` on the zone | Static files are collected into `staticfiles/` |  |  |  |
| G07 | Developer | uwsgi config | Review `/etc/uwsgi/uwsgi.ini` | `config.wsgi:application`, `chdir`, and `virtualenv` are set correctly |  |  |  |
| G08 | Developer | nginx static/media aliases | Review nginx config | `/static/` and `/media/` aliases point to correct paths |  |  |  |
| G09 | Developer | Service restart | Run `systemctl restart uwsgi` and `systemctl reload nginx` | Services restart without errors |  |  |  |
| G10 | Visitor | Deployment URL | Open deployed URL | Site loads |  |  |  |
| G11 | Demo users | Demo accounts | Login with demo accounts | Accounts work |  |  |  |
| G12 | All | Core workflow deployed | Test main workflows on deployed site | Core workflows function |  |  |  |
