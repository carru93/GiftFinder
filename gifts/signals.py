from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse

from users.models import Notification

from .models import Gift, Review, ReviewVote, SavedSearch
from .views import get_age_range


@receiver([post_save, post_delete], sender=Review)
def update_after_review_change(sender, instance, created, **kwargs):
    if created:
        receiver = instance.gift.suggestedBy
        if receiver is None:
            Notification.objects.create(
                user=receiver, notification_type="new_review", content_object=instance
            )
            channel_layer = get_channel_layer()
            notification_data = {
                "id": instance.id,
                "type": "new_review",
                "review_title": instance.title,
                "review_content": instance.content,
                "author_username": instance.author.username,
                "gift_id": instance.gift.id,
                "gift_name": instance.gift.name,
                "gift_url": instance.get_gift_url(),
                "content": instance.content,
                "timestamp": instance.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            async_to_sync(channel_layer.group_send)(
                f"user_{receiver.id}",
                {
                    "type": "send_notification",
                    "notification": notification_data,
                },
            )

    gift = instance.gift
    _update_gift_average_rating(gift)


@receiver([post_save, post_delete], sender=ReviewVote)
def update_after_review_vote_change(sender, instance, **kwargs):
    review = instance.review
    gift = review.gift
    _update_gift_average_rating(gift)


def _update_gift_average_rating(gift: Gift) -> None:
    """
    Updates the average rating of a given gift based on its reviews.

    Args:
        gift (Gift): The gift object whose average rating needs to be updated.
    Returns:
        None
    """

    reviews = gift.reviews.all()
    if not reviews.exists():
        gift.average_rating = 0.0
        gift.save()
        return

    total_weight = 0
    total_weighted_score = 0
    for review in reviews:
        local_weight = 1 + review.score if review.score > 0 else 1
        total_weight += local_weight
        total_weighted_score += review.rating * local_weight

    gift.average_rating = total_weighted_score / total_weight
    gift.save()


@receiver(post_save, sender=Gift)
def notify_saved_searches(sender, instance, created, **kwargs):
    if not created:
        return

    saved_searches = SavedSearch.objects.all()

    for search in saved_searches:
        matches = True

        if (
            search.category
            and instance.giftCategories.filter(id=search.category.id).count() == 0
        ):
            matches = False

        if search.price_min and instance.priceMax < search.price_min:
            matches = False

        if search.price_max and instance.priceMin > search.price_max:
            matches = False

        if search.age:
            age_range = get_age_range(search.age)
            if age_range not in [instance.suitable_age_range, "Any"]:
                matches = False

        if search.gender and instance.suitable_gender not in [search.gender, "U"]:
            matches = False

        if (
            search.location
            and search.location.lower() not in instance.suitable_location.lower()
        ):
            matches = False

        if search.hobbies.exists():
            if not instance.hobbies.filter(id__in=search.hobbies.all()).exists():
                matches = False

        if matches:
            notification = Notification.objects.create(
                user=search.user,
                notification_type="new_gift",
                content_object=instance,
                is_read=False,
            )

            channel_layer = get_channel_layer()
            notification_data = {
                "id": notification.id,
                "type": "new_gift",
                "gift_name": instance.name,
                "gift_description": instance.description,
                "gift_url": reverse("gifts:detail", kwargs={"pk": instance.id}),
                "timestamp": notification.timestamp.isoformat(),
            }
            async_to_sync(channel_layer.group_send)(
                f"user_{search.user.id}",
                {
                    "type": "send_notification",
                    "notification": notification_data,
                },
            )
