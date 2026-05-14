"""subscriptions app 的表单。"""
from django import forms

from .models import Organisation, Subscription


class SubscriptionForm(forms.ModelForm):
    """admin 管理 organisation 的 SaaS subscription。

    subscription 属于 organisation，因此表单需要选择 organisation。
    """

    class Meta:
        model = Subscription
        fields = ("organisation", "plan_name", "status", "start_date", "end_date")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date cannot be earlier than start date.")

        return cleaned_data


class OrganisationRequestForm(forms.ModelForm):
    """用户申请 organiser publishing access 的 organisation 表单。"""

    class Meta:
        model = Organisation
        fields = ("name", "description")
        labels = {
            "name": "Organisation name",
            "description": "Optional message",
        }
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Tell the admin anything helpful about your organiser request.",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Organisation name is required.")
        return name
