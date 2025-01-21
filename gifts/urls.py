from django.urls import path

from .views import (
    GiftCreateView,
    GiftDetailView,
    GiftUpdateView,
    ListGifts,
    ReviewCreateView,
    SearchGiftView,
    downvote_review,
    mark_as_owned,
    upvote_review,
)

app_name = "gifts"

urlpatterns = [
    path("", ListGifts.as_view(), name="list"),
    path("new/", GiftCreateView.as_view(), name="create"),
    path("search/", SearchGiftView.as_view(), name="search"),
    path("mark-as-owned/<int:pk>/", mark_as_owned, name="mark_as_owned"),
    path("gifts/<int:pk>/", GiftUpdateView.as_view(), name="gift_update"),
    path("detail/<int:pk>/", GiftDetailView.as_view(), name="detail"),
    path("detail/<int:pk>/review/new/", ReviewCreateView.as_view(), name="add_review"),
    path("review/<int:review_id>/upvote/", upvote_review, name="upvote_review"),
    path("review/<int:review_id>/downvote/", downvote_review, name="downvote_review"),
]
