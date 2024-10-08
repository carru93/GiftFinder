from django.urls import path

from .views import GiftCreateView, ListGifts, SearchGiftView

app_name = "gifts"

urlpatterns = [
    path("", ListGifts.as_view(), name="list"),
    path("new/", GiftCreateView.as_view(), name="create"),
    path("search/", SearchGiftView.as_view(), name="search"),
]
