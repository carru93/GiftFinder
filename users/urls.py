from django.urls import path

from .views import (
    FriendsListView,
    FriendsSearchView,
    Login,
    ProfileView,
    SuggestedGiftsView,
    UserDetailView,
    UserUpdateView,
    WishListView,
    logout_view,
    register,
    toggle_follow_user,
)

app_name = "users"

urlpatterns = [
    path("register/", register, name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/settings/", UserUpdateView.as_view(), name="settings"),
    path("profile/wishlist/", WishListView.as_view(), name="wishlist"),
    path("profile/friends/", FriendsListView.as_view(), name="friends"),
    path("profile/friends/search", FriendsSearchView.as_view(), name="search_friends"),
    path("<int:pk>", UserDetailView.as_view(), name="user"),
    path("follow/<int:pk>", toggle_follow_user, name="toggle_follow_user"),
    path("suggested/", SuggestedGiftsView.as_view(), name="suggested_gifts"),
]
