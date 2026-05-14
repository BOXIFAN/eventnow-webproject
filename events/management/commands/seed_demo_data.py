"""创建本地开发用的 demo data。"""
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import UserProfile
from events.models import Category, Event, Session, Venue
from subscriptions.models import Organisation, Subscription


class Command(BaseCommand):
    help = "Seed demo categories, venues, organisation, and subscription for local testing."

    def handle(self, *args, **options):
        self.stdout.write("Seeding EventNow demo data...")

        category_names = ["Workshop", "Networking", "Music", "Sports"]
        for name in category_names:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={"description": f"Demo category for {name.lower()} events."},
            )
            self._write_result("Category", category.name, created)

        venue_data = [
            {
                "name": "UQ Great Court",
                "address": "The University of Queensland, St Lucia",
                "city": "Brisbane",
                "room": "Outdoor Area",
            },
            {
                "name": "Advanced Engineering Building",
                "address": "The University of Queensland, St Lucia",
                "city": "Brisbane",
                "room": "Lecture Room",
            },
            {
                "name": "Student Union Hall",
                "address": "The University of Queensland, St Lucia",
                "city": "Brisbane",
                "room": "Main Hall",
            },
        ]
        for venue_values in venue_data:
            venue, created = Venue.objects.get_or_create(
                name=venue_values["name"],
                defaults=venue_values,
            )
            self._write_result("Venue", venue.name, created)

        organiser_profile = (
            UserProfile.objects.select_related("user")
            .filter(role=UserProfile.Role.ORGANISER)
            .order_by("created_at")
            .first()
        )

        if not organiser_profile:
            self.stdout.write(
                self.style.WARNING(
                    "No organiser user found. Register an organiser account before seeding organisation data."
                )
            )
            return

        organiser = organiser_profile.user
        organisation, created = Organisation.objects.get_or_create(
            name="Demo Student Society",
            defaults={
                "description": "Demo organisation for local EventNow testing.",
                "owner": organiser,
                "status": Organisation.Status.ACTIVE,
            },
        )
        self._write_result("Organisation", organisation.name, created)

        today = timezone.localdate()
        subscription, created = Subscription.objects.get_or_create(
            organisation=organisation,
            plan_name="Demo Plan",
            defaults={
                "status": Subscription.Status.ACTIVE,
                "start_date": today,
                "end_date": today + timedelta(days=365),
            },
        )
        self._write_result("Subscription", str(subscription), created)

        self._seed_demo_events(organisation, organiser)

        self.stdout.write(self.style.SUCCESS("Demo data seeding complete."))

    def _seed_demo_events(self, organisation, organiser):
        """创建 recommendation demo 所需的 published events 和 sessions。"""
        now = timezone.now()
        demo_events = [
            {
                "title": "Music Workshop",
                "category": "Music",
                "venue": "Student Union Hall",
                "days": 7,
                "status": Event.Status.PUBLISHED,
                "capacity": 30,
                "session_title": "Intro Music Jam",
            },
            {
                "title": "Music Networking Night",
                "category": "Music",
                "venue": "UQ Great Court",
                "days": 10,
                "status": Event.Status.PUBLISHED,
                "capacity": 40,
                "session_title": "Meet Local Musicians",
            },
            {
                "title": "Sports Meetup",
                "category": "Sports",
                "venue": "UQ Great Court",
                "days": 12,
                "status": Event.Status.PUBLISHED,
                "capacity": 35,
                "session_title": "Social Sports Session",
            },
            {
                "title": "Tech Career Talk",
                "category": "Workshop",
                "venue": "Advanced Engineering Building",
                "days": 14,
                "status": Event.Status.PUBLISHED,
                "capacity": 50,
                "session_title": "Career Q&A",
            },
            {
                "title": "Pending Admin Review Event",
                "category": "Networking",
                "venue": "Student Union Hall",
                "days": 18,
                "status": Event.Status.PENDING,
                "capacity": 25,
                "session_title": "Pending Review Session",
            },
        ]

        for event_values in demo_events:
            category = Category.objects.get(name=event_values["category"])
            venue = Venue.objects.get(name=event_values["venue"])
            start_datetime = now + timedelta(days=event_values["days"])
            end_datetime = start_datetime + timedelta(hours=2)

            event, created = Event.objects.get_or_create(
                title=event_values["title"],
                defaults={
                    "organisation": organisation,
                    "organiser": organiser,
                    "category": category,
                    "venue": venue,
                    "description": f"Demo event for recommendation testing: {event_values['title']}.",
                    "start_datetime": start_datetime,
                    "end_datetime": end_datetime,
                    "capacity": event_values["capacity"],
                    "price": 0,
                    "status": event_values["status"],
                },
            )
            self._write_result("Event", event.title, created)

            session, session_created = Session.objects.get_or_create(
                event=event,
                title=event_values["session_title"],
                defaults={
                    "description": f"Demo session for {event.title}.",
                    "start_datetime": event.start_datetime,
                    "end_datetime": event.start_datetime + timedelta(hours=1),
                    "capacity": max(10, min(event.capacity, 20)),
                },
            )
            self._write_result("Session", session.title, session_created)

    def _write_result(self, model_name, object_name, created):
        """输出每条 demo data 是新建还是已存在。"""
        action = "Created" if created else "Already exists"
        self.stdout.write(f"{action}: {model_name} - {object_name}")
