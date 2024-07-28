from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from gifts.models import Gift

from .forms import UserCreationForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(request.GET.get("next", "home"))
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "users/settings.html"


class WishListView(LoginRequiredMixin, TemplateView):
    template_name = "users/wishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["suggested_gifts"] = Gift.objects.filter(suggestedBy=self.request.user)
        return context
