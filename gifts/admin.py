from django.contrib import admin

from .models import (
    Gift,
    GiftCategory,
    Review,
    ReviewImage,
    ReviewVote,
    SavedSearch,
    WishList,
)


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
    filter_horizontal = ("giftCategories", "hobbies")

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


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)
    filter_horizontal = ("gifts",)


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "gift", "author", "rating", "created_at", "score_display")
    search_fields = ("gift__name", "author__username", "title", "content")
    list_filter = ("rating", "created_at")
    inlines = [ReviewImageInline]

    def score_display(self, obj):
        return obj.score  # property “score” = upvotes - downvotes

    score_display.short_description = "Score"


@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ("id", "review", "user", "vote")
    search_fields = ("review__gift__name", "user__username")
    list_filter = ("vote",)


@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at", "order_by")
    search_fields = ("name", "user__username", "location")
    list_filter = ("category", "gender", "created_at")
    filter_horizontal = ("hobbies",)
