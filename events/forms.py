"""events app 的表单。"""
import os

from django import forms

from accounts.decorators import get_user_role
from accounts.models import UserProfile
from subscriptions.models import Organisation

from .models import Category, Event, Registration, Session, SessionSelection, Venue


def get_session_remaining_capacity(session):
    """计算 session 剩余容量，只统计仍然 registered 的报名。"""
    selected_count = SessionSelection.objects.filter(
        session=session,
        registration__status=Registration.Status.REGISTERED,
    ).count()
    return max(session.capacity - selected_count, 0)


class EventForm(forms.ModelForm):
    """organiser 创建和编辑 event 的表单。"""

    class Meta:
        model = Event
        fields = (
            "organisation",
            "category",
            "venue",
            "title",
            "description",
            "image",
            "start_datetime",
            "end_datetime",
            "capacity",
            "price",
            "status",
        )
        widgets = {
            "start_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "description": forms.Textarea(attrs={"rows": 5}),
            "capacity": forms.NumberInput(attrs={"min": "1"}),
            "price": forms.NumberInput(attrs={"min": "0", "step": "0.01"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["start_datetime"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_datetime"].input_formats = ["%Y-%m-%dT%H:%M"]

        self.user = user
        # organiser 不出现在表单里，因为创建者必须由当前登录用户自动设置。
        self.fields["organisation"].help_text = "Choose the organisation that owns this event."
        self.fields["category"].help_text = "Categories are managed in Django Admin."
        self.fields["venue"].help_text = "Venues are managed in Django Admin."
        self.fields["image"].help_text = "Optional event image. Recommended for improving the event page appearance."
        self.fields["capacity"].help_text = "Capacity must be greater than 0."
        self.fields["price"].help_text = "Use 0 for free events."
        self.fields["status"].help_text = "Events created by organisers require admin approval before appearing publicly."

        organisations = Organisation.objects.exclude(status=Organisation.Status.ARCHIVED)

        self.has_publishing_access = True
        # organisation queryset 按 user 和 subscription 限制，organiser 可登录但必须有有效 subscription 才能创建 event。
        if user and user.is_authenticated:
            role = get_user_role(user)
            if not user.is_superuser and role != UserProfile.Role.ADMIN:
                active_org_ids = [
                    organisation.id
                    for organisation in organisations.filter(owner=user, status=Organisation.Status.ACTIVE)
                    if organisation.has_active_subscription()
                ]
                organisations = organisations.filter(id__in=active_org_ids)
                self.has_publishing_access = bool(active_org_ids)
                # event status 用于内容审核；subscription 用于平台使用资格，这是两层不同权限。
                self.fields["status"].choices = [
                    (Event.Status.DRAFT, "Draft"),
                    (Event.Status.PENDING, "Pending"),
                ]
                self.fields["status"].initial = Event.Status.PENDING
            else:
                organisations = organisations.filter(status=Organisation.Status.ACTIVE)

        if self.instance and self.instance.pk:
            organisations = (organisations | Organisation.objects.filter(id=self.instance.organisation_id)).distinct()

        self.fields["organisation"].queryset = organisations.order_by("name")
        self.fields["category"].queryset = Category.objects.order_by("name")
        self.fields["venue"].queryset = Venue.objects.order_by("city", "name")

        self.has_available_organisations = self.fields["organisation"].queryset.exists()
        self.has_available_categories = self.fields["category"].queryset.exists()
        self.has_available_venues = self.fields["venue"].queryset.exists()

    def clean_price(self):
        """前端表单层也检查 price，避免负数价格进入 model validation。"""
        price = self.cleaned_data.get("price")

        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative. Use 0 for free events.")

        return price

    def clean_image(self):
        """只做轻量图片格式和大小限制，不引入额外图片处理逻辑。"""
        image = self.cleaned_data.get("image")

        if not image:
            return image

        allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        file_extension = os.path.splitext(image.name)[1].lower()
        if file_extension not in allowed_extensions:
            raise forms.ValidationError("Event image must be a JPG, JPEG, PNG, or WEBP file.")

        if image.size > 3 * 1024 * 1024:
            raise forms.ValidationError("Event image must be smaller than 3MB.")

        return image


class SessionForm(forms.ModelForm):
    """organiser 创建和编辑 session 的表单。"""

    class Meta:
        model = Session
        fields = (
            "title",
            "description",
            "start_datetime",
            "end_datetime",
            "capacity",
        )
        widgets = {
            "start_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_datetime": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "description": forms.Textarea(attrs={"rows": 5}),
            "capacity": forms.NumberInput(attrs={"min": "1"}),
        }

    def __init__(self, *args, event=None, **kwargs):
        self.event = event
        super().__init__(*args, **kwargs)
        self.fields["start_datetime"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_datetime"].input_formats = ["%Y-%m-%dT%H:%M"]

        # event 不在表单中选择，因为 session 必须属于 URL 指定的 event。
        self.fields["capacity"].help_text = "Capacity must be greater than 0."

    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")
        capacity = cleaned_data.get("capacity")

        if capacity is not None and capacity <= 0:
            self.add_error("capacity", "Session capacity must be greater than 0.")

        # session 是 event 的子项，单个 session 容量不应超过 event 的总报名容量。
        if self.event and capacity is not None and capacity > self.event.capacity:
            self.add_error("capacity", "Session capacity cannot exceed the total event capacity.")

        if start_datetime and end_datetime and end_datetime <= start_datetime:
            self.add_error("end_datetime", "Session end datetime must be later than start datetime.")

        if self.event and start_datetime and end_datetime:
            if start_datetime < self.event.start_datetime or end_datetime > self.event.end_datetime:
                self.add_error(
                    "start_datetime",
                    "Session times should fit within the event schedule.",
                )

        return cleaned_data


class EventRegistrationForm(forms.Form):
    """普通用户报名 event 时选择 sessions 的表单。"""

    sessions = forms.ModelMultipleChoiceField(
        queryset=Session.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def __init__(self, *args, event=None, **kwargs):
        self.event = event
        super().__init__(*args, **kwargs)

        # sessions 根据当前 event 动态生成，避免用户选择其他 event 的 session。
        if event:
            sessions = event.sessions.order_by("start_datetime")
            self.fields["sessions"].queryset = sessions
            self.fields["sessions"].label_from_instance = self._session_label

    def _session_label(self, session):
        remaining_capacity = get_session_remaining_capacity(session)
        return (
            f"{session.title} | "
            f"{session.start_datetime:%b %d, %Y %H:%M} - {session.end_datetime:%H:%M} | "
            f"Remaining: {remaining_capacity}"
        )

    def clean_sessions(self):
        selected_sessions = self.cleaned_data.get("sessions")

        if not selected_sessions:
            raise forms.ValidationError("Please select at least one session.")

        for session in selected_sessions:
            if self.event and session.event_id != self.event.id:
                raise forms.ValidationError("Selected sessions must belong to this event.")

            # 必须检查 session capacity，避免超过 session 可容纳人数。
            if get_session_remaining_capacity(session) <= 0:
                raise forms.ValidationError("One or more selected sessions are full.")

        return selected_sessions
