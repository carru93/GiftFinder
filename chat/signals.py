from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Notification

from .models import Message


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        receiver = instance.receiver
        Notification.objects.create(
            user=receiver, notification_type="new_message", content_object=instance
        )

        channel_layer = get_channel_layer()
        notification_data = {
            "id": instance.id,
            "type": "new_message",
            "message": instance.content,
            "sender_id": instance.sender.id,
            "sender_username": instance.sender.username,
            "timestamp": instance.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "chat_url": instance.get_chat_url(),
        }
        async_to_sync(channel_layer.group_send)(
            f"user_{receiver.id}",
            {"type": "send_notification", "notification": notification_data},
        )
