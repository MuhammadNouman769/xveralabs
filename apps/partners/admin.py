import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import PartnerApplication


@admin.register(PartnerApplication)
class PartnerApplicationAdmin(admin.ModelAdmin):
    list_display = ("created_at", "reference", "full_name", "partner_type", "company", "region", "email", "status")
    list_editable = ("status",)
    list_filter = ("status", "partner_type", "region", "created_at")
    search_fields = ("full_name", "email", "company", "phone", "message")
    date_hierarchy = "created_at"
    fieldsets = (
        ("Application", {"fields": ("partner_type", "full_name", "email", "phone_code", "phone", "company", "region")}),
        ("Investor details", {"fields": ("module", "investment_range")}),
        ("Message", {"fields": ("message", "heard_from", "consent")}),
        ("Internal (not shown to the applicant)", {"fields": ("status", "internal_notes", "ip_address", "created_at", "updated_at")}),
    )
    readonly_fields = ("partner_type", "full_name", "email", "phone_code", "phone", "company", "region", "module",
                       "investment_range", "message", "heard_from", "consent", "ip_address", "created_at", "updated_at")
    actions = ["mark_contacted", "export_csv"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected as contacted")
    def mark_contacted(self, request, queryset):
        queryset.update(status="contacted")

    @admin.action(description="Export selected to CSV")
    def export_csv(self, request, queryset):
        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = 'attachment; filename="partner-applications.csv"'
        w = csv.writer(resp)
        w.writerow(["Reference", "Date", "Type", "Name", "Email", "Phone", "Company", "Region", "Module", "Range", "Status", "Message"])
        for a in queryset:
            w.writerow([a.reference, a.created_at.strftime("%Y-%m-%d %H:%M"), a.get_partner_type_display(), a.full_name,
                        a.email, a.full_phone, a.company, a.region, a.module, a.investment_range, a.status, a.message])
        return resp