from django import forms
from django.contrib.auth.forms import (
    UserChangeForm as ChangeForm,
    UserCreationForm as CreationForm,
)

from .models import User


class UserCreationForm(CreationForm):
    username = forms.CharField(label="username", min_length=5, max_length=150)
    email = forms.EmailField(label="email")
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class UserChangeForm(ChangeForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "bio",
            "birth_date",
            "public_wishlist",
            "hobbies",
        )


class UserSearchForm(forms.Form):
    class Meta:
        model = User
        fields = ("username",)
