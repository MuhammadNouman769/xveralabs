from django.contrib import admin

from .models import PartnerApplication


@admin.register(PartnerApplication)
class PartnerApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "partner_type", "email", "region", "status", "created_at")
    list_filter = ("partner_type", "status", "region", "created_at")
    search_fields = ("full_name", "email", "company", "message")
    list_editable = ("status",)
    readonly_fields = ("created_at", "consent")
    date_hierarchy = "created_at"
