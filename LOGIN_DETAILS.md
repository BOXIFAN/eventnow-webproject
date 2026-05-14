# EventNow Login Details

Deployment URL:

```text
https://s4752211-s4752211-eventnow.uqcloud.net
```

## Demo Accounts

| Account | Username | Password | Intended use |
|---|---|---|---|
| Primary marker/admin account | `superadmin` | `1403` | Main platform administrator account for marking. Use this account for the subscription workflow and platform-level admin testing. |
| Superuser | `superuser` | `82221789dd` | Site-level superuser account for ordinary event-related actions. It is not the primary admin account for marking, and it should not be described as the Django admin editing account. |
| Organiser | `organiser` | `82221789dd` | Organiser workflow account for organiser dashboard, event/session management, and subscription-controlled publishing access. |
| Attendee | `attendee` | `82221789dd` | Attendee workflow account for browsing events, registering for sessions, viewing registrations, and testing recommendations. |

## Quick Marker Workflow

1. Log in as `attendee` to test public browsing, registration, My Registrations, and Recommended Events.
2. Log in as `organiser` to test organiser dashboard, Manage Events, session management, and registration tracking.
3. Log in as `superadmin` to test Subscription Management and platform-level administrative workflows.
