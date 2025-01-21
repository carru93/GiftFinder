from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Gift, Review, ReviewVote


@receiver([post_save, post_delete], sender=Review)
def update_after_review_change(sender, instance, created, **kwargs):

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
