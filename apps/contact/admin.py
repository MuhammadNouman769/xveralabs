from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "full_name", "company", "topic", "region", "source", "email", "status")
    list_editable = ("status",)
    list_filter = ("status", "source", "topic", "region", "created_at")
    search_fields = ("full_name", "email", "company", "phone", "details")
    date_hierarchy = "created_at"
    readonly_fields = [f.name for f in ContactMessage._meta.fields if f.name != "status"]
    actions = ["mark_contacted"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected as contacted")
    def mark_contacted(self, request, queryset):
        queryset.update(status="contacted")