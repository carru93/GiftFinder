from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Notification


@receiver(post_save, sender=Notification)
def send_notification_email(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    notification_type = instance.notification_type

    notification_flag_map = {
        "new_message": ("email_new_message", "emails/notification_new_message.html"),
        "new_gift": ("email_new_gift", "emails/notification_new_gift.html"),
        "new_review": ("email_new_review", "emails/notification_new_review.html"),
    }

    flag, email_template = notification_flag_map.get(notification_type, (None, None))
    print(flag, email_template, getattr(user, flag, False), user.email)

    if flag and getattr(user, flag, False) and user.email:
        if settings.NOTIFICATIONS_EMAIL_ENABLED:
            recipient_email = user.email
        else:
            recipient_email = settings.NOTIFICATIONS_EMAIL_TEST_ADDRESS

        context = {
            "user": user,
            "timestamp": instance.timestamp,
        }

        if notification_type == "new_gift":
            gift = instance.content_object
            context.update(
                {
                    "gift_name": gift.name,
                    "gift_description": gift.description,
                    "gift_url": gift.get_absolute_url(),
                }
            )

        elif notification_type == "new_review":
            review = instance.content_object
            gift = review.gift
            context.update(
                {
                    "gift_name": gift.name,
                    "gift_description": gift.description,
                    "gift_url": review.get_gift_url(),
                    "review_content": review.content,
                }
            )

        elif notification_type == "new_message":
            message = instance.content_object
            context.update(
                {
                    "sender_username": message.sender.username,
                    "content": message.content,
                    "chat_url": message.get_chat_url(),
                }
            )

        else:
            return

        email_subject_map = {
            "new_message": "You have a new message",
            "new_gift": "A new gift matches your search",
            "new_review": "A new review is available",
        }

        email_subject = email_subject_map.get(notification_type, "New notification")

        email_body = render_to_string(email_template, context)

        send_mail(
            subject=email_subject,
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=email_body,
        )
