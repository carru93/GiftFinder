from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Message model.
    """

    list_display = ("id", "sender", "receiver", "room_name", "timestamp", "is_read")
    search_fields = ("sender__username", "receiver__username", "room_name", "content")
    list_filter = ("is_read", "timestamp")
    readonly_fields = ("timestamp",)

    fieldsets = (
        (None, {"fields": ("sender", "receiver", "room_name", "content")}),
        (
            "Status",
            {
                "fields": ("is_read", "timestamp"),
            },
        ),
    )
