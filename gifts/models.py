from django.conf import settings
from django.db import models


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
    """

    AGE_RANGE_CHOICES = [
        ("0-12", "Bambini (0-12)"),
        ("13-17", "Adolescenti (13-17)"),
        ("18-24", "Giovani Adulti (18-24)"),
        ("25-34", "Adulti (25-34)"),
        ("35-50", "Adulti (35-50)"),
        ("50+", "Senior (50+)"),
    ]
    GENDER_CHOICES = [
        ("M", "Maschio"),
        ("F", "Femmina"),
        ("O", "Altro"),
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

    def __str__(self):
        return str(self.name)


class WishList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gifts = models.ManyToManyField(Gift)


class GiftCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "gift categories"

    def __str__(self):
        return str(self.name)
