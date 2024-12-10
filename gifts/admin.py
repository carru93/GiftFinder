from django.contrib import admin

from .models import Gift, GiftCategory


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "suggestedBy",
        "price_range",
        "suitable_age_range",
        "suitable_gender",
        "suitable_location",
    )
    search_fields = (
        "name",
        "description",
        "suitable_location",
        "suggestedBy__username",
    )
    list_filter = ("giftCategories", "suitable_age_range", "suitable_gender", "hobbies")
    readonly_fields = ("suitable_age_range", "suitable_gender", "suitable_location")

    fieldsets = (
        (None, {"fields": ("name", "description", "image")}),
        (
            "Pricing & Categories",
            {"fields": ("priceMin", "priceMax", "giftCategories")},
        ),
        (
            "Hobbies & Suggestion Data",
            {
                "fields": (
                    "hobbies",
                    "suggestedBy",
                    "suitable_age_range",
                    "suitable_gender",
                    "suitable_location",
                ),
                "description": "These fields reflect the user’s attributes at the time of creation.",
            },
        ),
    )

    def price_range(self, obj):
        return f"${obj.priceMin} - ${obj.priceMax}"

    price_range.short_description = "Price Range"


@admin.register(GiftCategory)
class GiftCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
