from django.contrib import admin

from .models import Notification, User


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
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = (
        "hobbies",
        "friends",
        "possessed_gifts",
        "groups",
        "user_permissions",
    )

    fieldsets = (
        (
            None,
            {
                "fields": ("username", "email", "password"),
            },
        ),
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
        (
            "Preferences",
            {
                "fields": (
                    "public_wishlist",
                    "hobbies",
                    "friends",
                    "email_new_message",
                    "email_new_gift",
                    "email_new_review",
                )
            },
        ),
        (
            "Possessed gifts",
            {
                "fields": ("possessed_gifts",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
            },
        ),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Gestisce le notifiche in admin, permettendo di ricercarle e filtrare
    per tipo, stato di lettura, e data di creazione.
    """

    list_display = (
        "id",
        "user",
        "notification_type",
        "is_read",
        "timestamp",
        "content_object",
    )
    list_filter = (
        "notification_type",
        "is_read",
        "timestamp",
    )
    search_fields = ("user__username",)
    date_hierarchy = "timestamp"
    readonly_fields = ("timestamp",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "notification_type",
                    "content_type",
                    "object_id",
                    "content_object",
                    "is_read",
                    "timestamp",
                )
            },
        ),
    )
