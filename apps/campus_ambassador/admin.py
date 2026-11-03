import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Application, Cohort, ProgramItem, Story


@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ("name", "is_open", "opens_on", "closes_on", "term_months", "accepting", "applicants")
    list_editable = ("is_open",)

    @admin.display(boolean=True, description="Accepting now")
    def accepting(self, obj):
        return obj.is_accepting

    @admin.display(description="Applicants")
    def applicants(self, obj):
        return obj.applications.count()


@admin.register(ProgramItem)
class ProgramItemAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("kind", "is_active")
    search_fields = ("title", "text")


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ("name", "university", "label", "is_published", "order")
    list_editable = ("is_published", "order")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("created_at", "reference", "full_name", "university", "city", "year_of_study", "email", "status")
    list_editable = ("status",)
    list_filter = ("status", "cohort", "year_of_study", "created_at")
    search_fields = ("full_name", "email", "phone", "university", "city", "motivation")
    date_hierarchy = "created_at"
    fieldsets = (
        ("Applicant", {"fields": ("full_name", "email", "phone", "university", "city", "degree", "year_of_study", "social_url")}),
        ("Application", {"fields": ("cohort", "motivation", "experience", "is_student", "consent")}),
        ("Internal (not shown to the applicant)", {"fields": ("status", "internal_notes", "ip_address", "created_at", "updated_at")}),
    )
    readonly_fields = ("full_name", "email", "phone", "university", "city", "degree", "year_of_study", "social_url", "cohort",
                       "motivation", "experience", "is_student", "consent", "ip_address", "created_at", "updated_at")
    actions = ["mark_selected", "export_csv"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected as selected")
    def mark_selected(self, request, queryset):
        queryset.update(status="selected")

    @admin.action(description="Export selected to CSV")
    def export_csv(self, request, queryset):
        resp = HttpResponse(content_type="text/csv")
        resp["Content-Disposition"] = 'attachment; filename="ambassador-applications.csv"'
        w = csv.writer(resp)
        w.writerow(["Reference", "Date", "Name", "Email", "Phone", "University", "City", "Degree", "Year", "Profile", "Status", "Why join"])
        for a in queryset:
            w.writerow([a.reference, a.created_at.strftime("%Y-%m-%d %H:%M"), a.full_name, a.email, a.phone, a.university,
                        a.city, a.degree, a.get_year_of_study_display(), a.social_url, a.status, a.motivation])
        return resp