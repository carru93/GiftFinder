from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from gifts.models import Gift

from .forms import UserChangeForm, UserCreationForm
from .models import User


class Login(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Login failed. Please check your username and password."
        )
        return self.render_to_response(self.get_context_data(form=form))


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


class WishListView(LoginRequiredMixin, TemplateView):
    template_name = "users/wishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["suggested_gifts"] = Gift.objects.filter(suggestedBy=self.request.user)
        return context


class UserUpdateView(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = "users/settings.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user
