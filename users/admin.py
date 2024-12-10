from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "birth_date",
        "public_wishlist",
        "gender",
        "location",
    )
    search_fields = ("username", "email", "first_name", "last_name", "location")
    list_filter = ("gender", "public_wishlist", "hobbies")
    readonly_fields = (
        "date_joined",
        "last_login",
    )
    filter_horizontal = (
        "hobbies",
        "friends",
    )

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "bio",
                    "birth_date",
                    "gender",
                    "location",
                )
            },
        ),
        ("Preferences", {"fields": ("public_wishlist", "hobbies", "friends")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
