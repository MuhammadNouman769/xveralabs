from django.contrib import admin

from .models import ServiceBlock, ServiceGroup, ServicePage


class ServiceBlockInline(admin.StackedInline):
    model = ServiceBlock
    extra = 0
    fields = (("kind", "order", "is_active"), "title", "text")
    ordering = ("kind", "order")


@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ServicePage)
class ServicePageAdmin(admin.ModelAdmin):
    list_display = ("title", "group", "slug", "order", "is_published", "updated_at")
    list_editable = ("order", "is_published")
    list_filter = ("group", "is_published")
    search_fields = ("title", "tagline", "intro")
    inlines = [ServiceBlockInline]
    fieldsets = (
        (None, {"fields": ("group", "title", "short_title", "slug", "order", "is_published")}),
        ("Banner and overview", {"fields": ("tagline", "meta_description", "intro"),
                                  "description": "Formatting: blank line = new paragraph, '## ' = sub-heading, '- ' = bullet, "
                                                 "'1. ' = numbered list, **bold**, [link text](https://example.com)."}),
    )