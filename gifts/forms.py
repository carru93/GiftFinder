from django import forms

from .models import Gift


class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = [
            "name",
            "description",
            "priceMin",
            "priceMax",
            "giftCategories",
            "image",
            "hobbies",
        ]
