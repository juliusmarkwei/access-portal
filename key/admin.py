from django.contrib import admin
from .models import AccessKey


@admin.register(AccessKey)
class AccessKeyAdmin(admin.ModelAdmin):
    list_display = ("owner", "status", "key", "procurement_date", "expires_at")
    search_fields = ("key", "owner__email")
    list_filter = ("status", "owner__email", "procurement_date", "expires_at")
    ordering = ("-created_at",)
    readonly_fields = ("key", "owner", "created_at", "expires_at")
