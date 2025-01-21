from django.conf import settings
from django.db import models
from django.db.models import Sum


class Gift(models.Model):
    """
    Represents a gift item.
    Attributes:
        name (str): The name of the gift.
        description (str): The description of the gift.
        priceMin (Decimal): The minimum price of the gift.
        priceMax (Decimal): The maximum price of the gift.
        giftCategories (ManyToManyField): The categories associated with the gift.
        image (ImageField): The image of the gift.
        suggestedBy (ForeignKey): The user who suggested the gift.
        hobbies (ManyToManyField): The hobbies associated with the gift.
        suitable_age_range (str): The suitable age range for the gift.
        suitable_gender (str): The suitable gender for the gift.
        suitable_location (str): The suitable location for the gift.
    """

    AGE_RANGE_CHOICES = [
        ("0-12", "Children (0-12)"),
        ("13-17", "Teenagers (13-17)"),
        ("18-24", "Young Adults (18-24)"),
        ("25-34", "Adults (25-34)"),
        ("35-50", "Adults (35-50)"),
        ("50+", "Seniors (50+)"),
    ]
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("U", "Unisex"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    priceMin = models.DecimalField(max_digits=10, decimal_places=2)
    priceMax = models.DecimalField(max_digits=10, decimal_places=2)
    giftCategories = models.ManyToManyField("GiftCategory", blank=True)
    image = models.ImageField(upload_to="gifts/", blank=True, null=True)
    suggestedBy = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    hobbies = models.ManyToManyField("hobbies.Hobby", blank=True)
    suitable_age_range = models.CharField(
        max_length=10, choices=AGE_RANGE_CHOICES, blank=True
    )
    suitable_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    suitable_location = models.CharField(max_length=100, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.name)


class WishList(models.Model):
    """
    Represents a user's wish list.
    Attributes:
        user (OneToOneField): A one-to-one relationship to the user who owns the wish list.
        gifts (ManyToManyField): A many-to-many relationship to the gifts included in the wish list.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gifts = models.ManyToManyField(Gift)


class GiftCategory(models.Model):
    """
    Represents a category of gifts.
    Attributes:
        name (str): The name of the category.
    """

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "gift categories"

    def __str__(self):
        return str(self.name)


class Review(models.Model):
    """
    Represents a review of a gift.
    Attributes:
        gift (ForeignKey): The gift being reviewed.
        author (ForeignKey): The user who wrote the review.
        title (str): The title of the review.
        content (str): The content of the review.
        rating (int): The rating given by the user.
        created_at (DateTimeField): The date and time the review was
    """

    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    gift = models.ForeignKey(Gift, related_name="reviews", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} on {self.gift.name} by {self.author.username}"

    @property
    def score(self):
        """upvotes - downvotes"""
        return ReviewVote.aggregate_sum_by_review(self)


class ReviewImage(models.Model):
    """
    Represents an image associated with a review.
    Attributes:
        review (ForeignKey): The review the image is associated with.
        image (ImageField): The image file.
    """

    review = models.ForeignKey(Review, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="reviews/")

    def __str__(self):
        return f"Image {self.id} for Review {self.review.id}"


class ReviewVote(models.Model):
    VOTE_CHOICES = ((1, "Upvote"), (-1, "Downvote"))
    review = models.ForeignKey(Review, related_name="votes", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("review", "user")

    def __str__(self):
        return f"Vote {self.vote} by {self.user.username} on Review {self.review.pk}"

    @staticmethod
    def aggregate_sum_by_review(review):
        result = ReviewVote.objects.filter(review=review).aggregate(Sum("vote"))
        total = result["vote__sum"] or 0
        return total
