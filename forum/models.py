from django.conf import settings
from django.db import models


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.content)[:30]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return str(self.name)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="comments", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.content)[:30]
