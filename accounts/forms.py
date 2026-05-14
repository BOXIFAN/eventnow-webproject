"""accounts app 的表单。"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class RegisterForm(UserCreationForm):
    """用户注册表单，注册时同步创建 UserProfile。"""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        """保存 User，并为用户创建或更新 UserProfile。

        普通用户不能自行注册为 organiser，因为 organiser 拥有 event 管理权限，
        必须由平台管理员审核后在 UserProfile 中手动批准。
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={"role": UserProfile.Role.ATTENDEE},
            )

        return user
