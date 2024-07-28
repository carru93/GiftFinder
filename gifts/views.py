from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import GiftForm
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
        return super().form_valid(form)
