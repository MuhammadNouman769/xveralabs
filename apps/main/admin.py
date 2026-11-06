from django.contrib import admin

from .models import IndustryCaseStudy, IndustryCaseStudyBlock


class IndustryCaseStudyBlockInline(admin.StackedInline):
    model = IndustryCaseStudyBlock
    extra = 0
    fields = ("kind", "order", "is_active", "title", "text")


@admin.register(IndustryCaseStudy)
class IndustryCaseStudyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_published", "updated_at")
    list_editable = ("order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("name", "title", "summary", "challenge", "approach")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [IndustryCaseStudyBlockInline]
    fieldsets = (
        (None, {"fields": ("name", "slug", "eyebrow", "order", "is_published")}),
        ("Content", {"fields": ("title", "summary", "challenge", "approach")}),
        ("Industry image", {"fields": ("image_url", "image_alt")}),
    )
