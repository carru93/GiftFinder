from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")
    search_fields = ("title", "content", "author__username", "author__email")
    list_filter = ("author", "created_at")
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("title", "content", "author")}),
        (
            "Dates",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse"),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("short_content", "post", "author", "created_at", "updated_at")
    search_fields = ("content", "author__username", "author__email", "post__title")
    list_filter = ("author", "post", "created_at")
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("post", "author", "content")}),
        ("Dates", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    readonly_fields = ("created_at", "updated_at")

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    short_content.short_description = "Comment Excerpt"
