from django.urls import path

from .views import Login, ProfileView, SettingsView, WishListView, logout_view, register

app_name = "users"

urlpatterns = [
    path("register/", register, name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/settings/", SettingsView.as_view(), name="settings"),
    path("profile/wishlist/", WishListView.as_view(), name="wishlist"),
]
