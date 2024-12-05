from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from dal.autocomplete import ModelSelect2Multiple
from django import forms

from hobbies.models import Hobby

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
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        required=False,
        widget=ModelSelect2Multiple(url="hobbies:autocomplete"),
        label="Hobbies",
    )
    age = forms.IntegerField(
        required=False,
        label="Age",
        min_value=0,
        max_value=120,
    )
    gender = forms.ChoiceField(
        choices=[("", "Any")] + Gift.GENDER_CHOICES,
        required=False,
        label="Gender",
    )
    location = forms.CharField(
        required=False,
        label="Location",
        max_length=100,
    )

    def __init__(self, *args, **kwargs):
        super(GiftSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("category", css_class="w-full md:w-1/4 px-2"),
                Column("price_min", css_class="w-full md:w-1/4 px-2"),
                Column("price_max", css_class="w-full md:w-1/4 px-2"),
                Column("age", css_class="w-full md:w-1/4 px-2"),
                css_class="flex flex-wrap -mx-2",
            ),
            Row(
                Column("gender", css_class="w-full md:w-1/4 px-2"),
                Column("location", css_class="w-full md:w-1/4 px-2"),
                Column("hobbies", css_class="w-full md:w-1/4 px-2"),
                Column(css_class="w-full md:w-1/4 px-2"),
                css_class="flex flex-wrap -mx-2",
            ),
        )
        self.helper.field_template = "tailwind/field.html"
