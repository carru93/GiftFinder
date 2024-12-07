from django.urls import path

from .views import (
    GiftCreateView,
    GiftUpdateView,
    ListGifts,
    SearchGiftView,
    mark_as_owned,
)

app_name = "gifts"

urlpatterns = [
    path("", ListGifts.as_view(), name="list"),
    path("new/", GiftCreateView.as_view(), name="create"),
    path("search/", SearchGiftView.as_view(), name="search"),
    path("mark-as-owned/<int:pk>/", mark_as_owned, name="mark_as_owned"),
    path("gifts/<int:pk>/", GiftUpdateView.as_view(), name="gift_update"),
]
