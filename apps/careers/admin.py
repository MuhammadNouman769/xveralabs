import csv

from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html

from .models import JobApplication, JobPosition


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "job_type", "work_mode", "level", "is_open", "is_featured", "deadline", "applicants")
    list_editable = ("is_open", "is_featured")
    list_filter = ("is_open", "job_type", "department", "work_mode", "level")
    search_fields = ("title", "summary", "description")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    actions = ["open_selected", "close_selected"]
    fieldsets = (
        (None, {"fields": ("title", "slug", "is_open", "is_featured", "deadline")}),
        ("Details", {"fields": ("department", "job_type", "work_mode", "level", "location", "duration", "compensation")}),
        ("Content", {"fields": ("summary", "description", "responsibilities", "requirements", "nice_to_have")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_apps=Count("applications"))

    @admin.display(description="Applicants", ordering="_apps")
    def applicants(self, obj):
        return obj._apps

    @admin.action(description="Open selected positions")
    def open_selected(self, request, queryset):
        queryset.update(is_open=True)

    @admin.action(description="Close selected positions")
    def close_selected(self, request, queryset):
        queryset.update(is_open=False)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("created_at", "reference", "full_name", "role", "city", "email", "cv_link", "status")
    list_editable = ("status",)
    list_filter = ("status", "position", "created_at")
    search_fields = ("full_name", "email", "phone", "position_title", "cover_note")
    date_hierarchy = "created_at"
    fieldsets = (
        ("Applicant", {"fields": ("full_name", "email", "phone", "city", "profile_url", "cv_link")}),
        ("Application", {"fields": ("position", "position_title", "cover_note", "consent")}),
        ("Internal (not shown to the applicant)", {"fields": ("status", "internal_notes", "ip_address", "created_at", "updated_at")}),
    )
    readonly_fields = ("full_name", "email", "phone", "city", "profile_url", "cv_link", "position", "position_title",
                       "cover_note", "consent", "ip_address", "created_at", "updated_at")
    actions = ["mark_shortlisted", "export_csv"]

    def has_add_permission(self, request):
        return False

    @admin.display(description="Role")
    def role(self, obj):
        return obj.position_title or "General application"

    @admin.display(description="CV")
    def cv_link(self, obj):
        if not obj.pk or not obj.cv:
            return "-"
        return format_html('<a href="{}">Download CV</a>', reverse("career_cv", args=[obj.pk]))

    @admin.action(description="Mark selected as shortlisted")
    def mark_shortlisted(self, request, queryset):
        queryset.update(status="shortlisted")

    @admin.action(description="Export selected to CSV")
    def export_csv(self, request, queryset):
        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = 'attachment; filename="job-applications.csv"'
        w = csv.writer(resp)
        w.writerow(["Reference", "Date", "Role", "Name", "Email", "Phone", "City", "Profile", "Status", "Note"])
        for a in queryset:
            w.writerow([a.reference, a.created_at.strftime("%Y-%m-%d %H:%M"), a.position_title or "General", a.full_name,
                        a.email, a.phone, a.city, a.profile_url, a.status, a.cover_note])
        return resp