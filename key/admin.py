from django.contrib import admin
from .models import AccessKey


@admin.register(AccessKey)
class AccessKeyAdmin(admin.ModelAdmin):
    list_display = ("owner", "status", "key", "procurement_date", "expiry_date")
    search_fields = ("key", "owner__email")
    list_filter = ("status", "owner__email", "procurement_date", "expiry_date")
    ordering = ("-created_at",)
    readonly_fields = ("key", "owner", "created_at", "expiry_date")
