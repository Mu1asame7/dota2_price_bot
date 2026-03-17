from django.contrib import admin
from .models import TelegramUser, ItemQuery


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "first_name", "last_name", "created_at")
    list_filter = ("created_at",)
    search_fields = ("username", "first_name", "last_name", "user_id")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(ItemQuery)
class ItemQueryAdmin(admin.ModelAdmin):
    list_display = ("item_name", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("item_name", "user__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
