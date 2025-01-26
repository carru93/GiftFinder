from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from gifts.models import Gift


class User(AbstractUser):
    """
    User model that extends the AbstractUser model to include additional fields and relationships.
    Attributes:
        bio (TextField): A brief biography of the user, optional max 500 characters.
        location (CharField): The user's location, optional max 30 characters.
        birth_date (DateField): The user's birth date, optional.
        groups (ManyToManyField): The groups this user belongs to, related to the auth.Group model.
        user_permissions (ManyToManyField): Specific permissions for this user, related to the auth.Permission model.
        public_wishlist (BooleanField): Indicates if the user's wishlist is public, defaults to False.
        hobbies (ManyToManyField): The user's hobbies, related to the hobbies.Hobby model.
        friends (ManyToManyField): The user's friends, related to the User model itself.
        gender (CharField): The user's gender, optional with choices defined in GENDER_CHOICES.
        possessed_gifts (ManyToManyField): The gifts possessed by the user, related to the Gift model.
    """

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("N", "Rather not say"),
    ]

    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    public_wishlist = models.BooleanField(default=False)
    hobbies = models.ManyToManyField("hobbies.Hobby", related_name="users", blank=True)
    friends = models.ManyToManyField("self", blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    possessed_gifts = models.ManyToManyField(Gift, blank=True, related_name="owners")
    email_new_message = models.BooleanField(default=False)
    email_new_gift = models.BooleanField(default=False)
    email_new_review = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("new_message", "New Message"),
        ("new_gift", "New Gift Matching Search"),
        ("new_review", "New Review"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification_type}"
