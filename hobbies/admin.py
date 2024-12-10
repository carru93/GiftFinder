from django.contrib import admin

from .models import Hobby


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
