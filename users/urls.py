from django.contrib.auth.views import LoginView
from django.urls import path

from .views import ProfileView, SettingsView, WishListView, logout_view, register

app_name = "users"

urlpatterns = [
    path("register/", register, name="signup"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/settings/", SettingsView.as_view(), name="settings"),
    path("profile/wishlist/", WishListView.as_view(), name="wishlist"),
]
