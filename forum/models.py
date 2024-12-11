from django.conf import settings
from django.db import models


class Post(models.Model):
    """
    Represents a forum post.
    Attributes:
        title (str): The title of the post, with a maximum length of 100 characters.
        content (str): The content of the post.
        created_at (datetime): The date and time when the post was created. Automatically set.
        updated_at (datetime): The date and time when the post was last updated.
        author (User): The user who authored the post.
    """

    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    """
    Represents a comment made by a user on a post.
    Attributes:
        content (TextField): The content of the comment.
        created_at (DateTimeField): The date and time when the comment was created.
        updated_at (DateTimeField): The date and time when the comment was last updated.
        post (ForeignKey): The post to which the comment belongs.
        author (ForeignKey): The user who authored the comment.
    """

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="comments", on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.content)[:30]
