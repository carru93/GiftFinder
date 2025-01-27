from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import CommentCreateForm, PostCreateForm
from .mixins import ModeratorRequiredMixin
from .models import Comment, Post


class ListPosts(ListView):
    model = Post
    template_name = "forum/list.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-created_at")
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).distinct()
        return queryset


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "forum/create.html"
    success_url = reverse_lazy("forum:list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "The post has been created!")
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = "forum/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.object).order_by(
            "-created_at"
        )
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "forum/create_comment.html"

    def form_valid(self, form):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        form.instance.author = self.request.user
        form.instance.post = post

        messages.success(self.request, "Comment added!")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("forum:post_detail", kwargs={"pk": self.object.post.id})


class PostDeleteView(ModeratorRequiredMixin, DeleteView):
    model = Post
    template_name = "forum/post_confirm_delete.html"
    success_url = reverse_lazy("forum:list")


class CommentDeleteView(ModeratorRequiredMixin, DeleteView):
    model = Comment
    template_name = "forum/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("forum:post_detail", kwargs={"pk": self.object.post.id})
