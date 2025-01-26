from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Message(models.Model):
    """
    Message model representing a chat message between users.

    Attributes:
        sender (ForeignKey): Reference to the user who sent the message.
        receiver (ForeignKey): Reference to the user who received the message.
        content (TextField): The content of the message.
        timestamp (DateTimeField): The time when the message was sent.
        is_read (BooleanField): Indicates whether the message has been read.

    Methods:
        __str__(): Returns a string representation of the message.
    """

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    room_name = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Msg from {self.sender} to {self.receiver} at {self.timestamp}"

    def get_chat_url(self):
        return f"{settings.SITE_URL}{reverse("chat:chat_room", kwargs={"pk": self.sender.id})}"
