from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Column, Div, Layout, Row, Submit
from dal.autocomplete import ModelSelect2Multiple
from django import forms
from django.contrib.auth.forms import UserCreationForm as CreationForm

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


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "bio",
            "birth_date",
            "public_wishlist",
            "hobbies",
            "gender",
            "location",
        )
        labels = {
            "bio": "Bio",
            "birth_date": "Birth Date",
            "public_wishlist": "Public Wishlist",
            "hobbies": "Hobbies",
            "gender": "Gender",
            "location": "Location",
        }
        widgets = {
            "hobbies": ModelSelect2Multiple(url="hobbies:autocomplete"),
            "birth_date": forms.DateInput(
                attrs={"type": "date", "class": "form-input"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.label_class = "text-white mb-0"
        self.fields["username"].help_text = ""
        # self.fields["username"].help_text = (
        #     f'<span class="text-white">{self.fields["username"].help_text}</span>'
        # )
        self.helper.layout = Layout(
            Row(
                Column("username", css_class="w-full md:w-1/2 px-2"),
                Column("email", css_class="w-full md:w-1/2 px-2"),
                css_class="flex flex-wrap mb-2 -mx-2",
            ),
            Row(
                Column("bio", css_class="w-full md:w-1/2 px-2"),
                Column("birth_date", css_class="w-full md:w-1/2 px-2"),
                css_class="flex flex-wrap mb-2 -mx-2",
            ),
            Row(
                Column("public_wishlist", css_class="w-full md:w-1/2 px-2"),
                Column("hobbies", css_class="w-full md:w-1/2 px-2"),
                css_class="flex flex-wrap mb-2 -mx-2",
            ),
            Row(
                Column("gender", css_class="w-full md:w-1/2 px-2"),
                Column("location", css_class="w-full md:w-1/2 px-2"),
                css_class="flex flex-wrap mb-2 -mx-2",
            ),
            Div(
                Button(
                    "cancel",
                    "Cancel",
                    css_class="ng-btn-secondary",
                    onclick="window.history.back()",
                ),
                Submit("submit", "Update", css_class="ng-btn"),
                css_class="flex justify-end space-x-2",
            ),
        )


class UserSearchForm(forms.Form):
    class Meta:
        model = User
        fields = ("username",)
