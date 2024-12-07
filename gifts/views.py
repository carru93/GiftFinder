from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import GiftFormCreate, GiftSearchForm
from .models import Gift


class ListGifts(ListView):
    model = Gift
    template_name = "gifts/gifts.html"


def calculate_age(birth_date):
    today = date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return age


def get_age_range(age):
    if age <= 12:
        return "0-12"
    if 13 <= age <= 17:
        return "13-17"
    if 18 <= age <= 24:
        return "18-24"
    if 25 <= age <= 34:
        return "25-34"
    if 35 <= age <= 50:
        return "35-50"
    return "50+"


class GiftCreateView(LoginRequiredMixin, CreateView):
    model = Gift
    form_class = GiftFormCreate
    template_name = "gifts/create.html"
    success_url = reverse_lazy("users:wishlist")

    def form_valid(self, form):
        user = self.request.user
        form.instance.suggestedBy = user

        response = super().form_valid(form)
        form.instance.hobbies.set(self.request.user.hobbies.all())

        if user.birth_date:
            age = calculate_age(user.birth_date)
            age_range = get_age_range(age)
            form.instance.suitable_age_range = age_range

        if user.gender:
            form.instance.suitable_gender = user.gender

        if user.location:
            form.instance.suitable_location = user.location

        form.instance.save()
        return response


class SearchGiftView(ListView):
    model = Gift
    template_name = "gifts/search.html"
    context_object_name = "gifts"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = GiftSearchForm(self.request.GET or None)

        if form.is_valid():
            category = form.cleaned_data.get("category")
            price_min = form.cleaned_data.get("price_min")
            price_max = form.cleaned_data.get("price_max")
            age = form.cleaned_data.get("age")
            gender = form.cleaned_data.get("gender")
            location = form.cleaned_data.get("location")

            if category:
                queryset = queryset.filter(giftCategories=category)
            if price_min is not None:
                queryset = queryset.filter(priceMin__gte=price_min)
            if price_max is not None:
                queryset = queryset.filter(priceMax__lte=price_max)
            if "hobbies" in self.request.GET and self.request.GET.getlist("hobbies"):
                queryset = queryset.filter(
                    hobbies__in=self.request.GET.getlist("hobbies")
                ).distinct()
            if age is not None:
                # Filtra i regali adatti alla fascia d'età
                age_ranges = []
                if age <= 12:
                    age_ranges.append("0-12")
                elif 13 <= age <= 17:
                    age_ranges.append("13-17")
                elif 18 <= age <= 24:
                    age_ranges.append("18-24")
                elif 25 <= age <= 34:
                    age_ranges.append("25-34")
                elif 35 <= age <= 50:
                    age_ranges.append("35-50")
                else:
                    age_ranges.append("50+")
                queryset = queryset.filter(suitable_age_range__in=age_ranges)
            if gender:
                queryset = queryset.filter(suitable_gender__in=[gender, "U"])
            if location:
                queryset = queryset.filter(suitable_location__icontains=location)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GiftSearchForm(self.request.GET or None)
        return context


@login_required
def mark_as_owned(request, pk):
    gift = get_object_or_404(Gift, pk=pk)
    user = request.user
    if gift not in user.possessed_gifts.all():
        user.possessed_gifts.add(gift)
        messages.success(request, "Gift marked as owned.")
    else:
        messages.info(request, "You already own this gift.")
    return redirect(request.META.get("HTTP_REFERER", "gifts:search"))
