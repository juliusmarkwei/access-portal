from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "email",
        "phone",
        "is_active",
        "is_admin",
        "created_at",
        "updated_at",
    ]
    search_fields = ["full_name", "email"]
    list_filter = ["is_active", "is_admin"]
    ordering = ["-created_at"]
