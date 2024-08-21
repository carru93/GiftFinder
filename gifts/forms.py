from django import forms

from .models import Gift, GiftCategory


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
        ]


class GiftSearchForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=GiftCategory.objects.all(),
        required=False,
        label="Gift Category",
        empty_label="Select a category",
    )
    price_min = forms.DecimalField(
        required=False,
        label="Minimum Price",
        min_value=0,
        max_digits=10,
        decimal_places=2,
    )
    price_max = forms.DecimalField(
        required=False,
        label="Maximum Price",
        min_value=0,
        max_digits=10,
        decimal_places=2,
    )
