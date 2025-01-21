from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Column, Div, Layout, Row, Submit
from dal.autocomplete import ModelSelect2Multiple
from django import forms

from hobbies.models import Hobby

from .models import Gift, GiftCategory, Review


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
        labels = {
            "name": "Gift Name",
            "description": "Description",
            "priceMin": "Minimum Price",
            "priceMax": "Maximum Price",
            "giftCategories": "Gift Categories",
            "image": "Image",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter gift name"}),
            "description": forms.Textarea(
                attrs={"placeholder": "Enter gift description"}
            ),
            "priceMin": forms.NumberInput(attrs={"placeholder": "Enter minimum price"}),
            "priceMax": forms.NumberInput(attrs={"placeholder": "Enter maximum price"}),
        }

    def __init__(self, *args, **kwargs):
        submit_text = kwargs.pop("submit_text", "Submit")
        super(GiftForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.label_class = "text-white mb-0"
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="w-full mb-2 md:w-1/2 px-2 text-primary"),
                Column("giftCategories", css_class="w-full mb-2 md:w-1/2 px-2"),
            ),
            Row(
                Column("description", css_class="w-full mb-2 px-2"),
            ),
            Row(
                Column("priceMin", css_class="w-full mb-2 md:w-1/2 px-2"),
                Column("priceMax", css_class="w-full mb-2 md:w-1/2 px-2"),
            ),
            Row(
                Column("image", css_class="w-full mb-2 px-2"),
            ),
            Div(
                Button(
                    "cancel",
                    "Cancel",
                    css_class="ng-btn-secondary",
                    onclick="window.history.back()",
                ),
                Submit("submit", submit_text, css_class="ng-btn"),
                css_class="flex justify-end space-x-2",
            ),
        )


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
        self.helper.label_class = "text-white mb-0"
        self.helper.layout = Layout(
            Row(
                Column("category", css_class="w-full md:w-1/4 px-2"),
                Column("price_min", css_class="w-full md:w-1/4 px-2"),
                Column("price_max", css_class="w-full md:w-1/4 px-2"),
                Column("age", css_class="w-full md:w-1/4 px-2"),
                css_class="flex flex-wrap -mx-2 mb-4",
            ),
            Row(
                Column("gender", css_class="w-full md:w-1/4 px-2"),
                Column("location", css_class="w-full md:w-1/4 px-2"),
                Column("hobbies", css_class="w-full md:w-1/4 px-2"),
                Column(css_class="w-full md:w-1/4 px-2"),
                css_class="flex flex-wrap -mx-2 mb-4",
            ),
        )
        self.helper.field_template = "tailwind/field.html"


class ReviewForm(forms.ModelForm):
    images = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={"allow_multiple_selected": True}),
        label="Review Images",
    )

    class Meta:
        model = Review
        fields = ["title", "content", "rating"]
        labels = {
            "title": "Title",
            "content": "Review",
            "rating": "Rating (1-5)",
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.label_class = "text-white mb-0"
        self.helper.layout = Layout(
            Row(
                Column("title", css_class="w-full mb-2 px-2"),
            ),
            Row(
                Column("content", css_class="w-full mb-2 px-2"),
            ),
            Row(
                Column("rating", css_class="w-full mb-2 px-2"),
            ),
            Row(
                Column("images", css_class="w-full mb-2 px-2"),
            ),
            Div(
                Button(
                    "cancel",
                    "Cancel",
                    css_class="ng-btn-secondary",
                    onclick="window.history.back()",
                ),
                Submit("submit", "Submit Review", css_class="ng-btn"),
                css_class="flex justify-end space-x-2",
            ),
        )
