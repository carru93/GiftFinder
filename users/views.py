from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, TemplateView, UpdateView

from gifts.models import Gift
from gifts.views import calculate_age, get_age_range

from .forms import UserChangeForm, UserCreationForm, UserSearchForm
from .models import Notification, User


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


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = "users/settings.html"
    success_url = reverse_lazy("users:settings")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)


class FriendsListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/list_friends.html"
    context_object_name = "friends"

    def get_queryset(self):
        return self.request.user.friends.all()


class FriendsSearchView(LoginRequiredMixin, ListView):
    model = User
    template_name = "users/search.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(id=self.request.user.id)
        friend_ids = self.request.user.friends.values_list("id", flat=True)
        queryset = queryset.exclude(id__in=friend_ids)

        if "filter" in self.request.GET:
            search_term = self.request.GET["filter"]
            queryset = queryset.filter(
                Q(username__icontains=search_term)
                | Q(first_name__icontains=search_term)
                | Q(last_name__icontains=search_term)
                | Q(email__icontains=search_term)
            )

        queryset = queryset.order_by("username")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserSearchForm(self.request.GET or None)
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user.html"
    context_object_name = "target"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wished_gifts"] = Gift.objects.filter(suggestedBy=self.kwargs["pk"])
        context["is_friend"] = self.request.user.friends.filter(
            id=self.kwargs["pk"]
        ).exists()
        return context


class SuggestedGiftsView(LoginRequiredMixin, ListView):
    model = Gift
    template_name = "users/suggested_gifts.html"
    context_object_name = "gifts"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Gift.objects.all()

        queryset = queryset.exclude(suggestedBy=user)
        queryset = queryset.exclude(
            id__in=user.possessed_gifts.values_list("id", flat=True)
        )

        filters = Q()

        if user.hobbies.exists():
            filters &= Q(hobbies__in=user.hobbies.all())

        if user.birth_date:
            age = calculate_age(user.birth_date)
            age_range = get_age_range(age)
            filters &= Q(suitable_age_range__in=[age_range])

        if user.gender:
            filters &= Q(suitable_gender__in=[user.gender, "U"])

        if user.location:
            filters &= Q(suitable_location__icontains=user.location)

        queryset = queryset.filter(filters).distinct()
        queryset = queryset.order_by("-average_rating")

        return queryset


@require_POST
def toggle_follow_user(request, pk):
    user = request.user
    target_user = User.objects.get(pk=pk)

    if user.friends.filter(pk=pk).exists():
        user.friends.remove(target_user)
        messages.success(request, f"You have unfollowed {target_user.username}.")
    else:
        user.friends.add(target_user)
        messages.success(request, f"You are now following {target_user.username}.")

    return redirect("users:user", pk=pk)


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by(
        "-timestamp"
    )[:10]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(
        request,
        "partials/notifications.html",
        {"notifications": notifications, "unread_count": unread_count},
    )


@require_POST
@login_required
def mark_notification_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
