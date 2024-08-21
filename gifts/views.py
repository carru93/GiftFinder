from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import GiftForm, GiftSearchForm
from .models import Gift


class ListGifts(ListView):
    model = Gift
    template_name = "gifts/gifts.html"


class GiftCreateView(LoginRequiredMixin, CreateView):
    model = Gift
    form_class = GiftForm
    template_name = "gifts/create.html"
    success_url = reverse_lazy("users:wishlist")

    def form_valid(self, form):
        form.instance.suggestedBy = self.request.user
        response = super().form_valid(form)
        form.instance.hobbies.set(self.request.user.hobbies.all())
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

            if category:
                queryset = queryset.filter(giftCategories=category)
            if price_min is not None:
                queryset = queryset.filter(priceMin__gte=price_min)
            if price_max is not None:
                queryset = queryset.filter(priceMax__lte=price_max)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GiftSearchForm(self.request.GET or None)
        return context
