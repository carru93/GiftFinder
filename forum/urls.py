from django.urls import path

from .views import CommentCreateView, ListPosts, PostCreateView, PostDetailView

app_name = "forum"

urlpatterns = [
    path("", ListPosts.as_view(), name="list"),
    path("new/", PostCreateView.as_view(), name="create"),
    path("<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("<int:post_id>/comments/new", CommentCreateView.as_view(), name="add_comment"),
]
