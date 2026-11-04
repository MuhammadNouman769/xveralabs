from django.db import models
from django.urls import reverse
from apps.utils.models import BaseModel
from .routes import SERVICE_ROUTES


class ServiceGroup(BaseModel):
    name = models.CharField(max_length=80, help_text="e.g. Strategy & Consulting")
    slug = models.SlugField(unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta: # type: ignore
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class ServicePage(BaseModel):
    group = models.ForeignKey(ServiceGroup, on_delete=models.PROTECT, related_name="pages")
    title = models.CharField(max_length=120, help_text="Page heading, e.g. Product Strategy")
    short_title = models.CharField(max_length=40, blank=True, help_text="Used in the small tabs, e.g. Product")
    slug = models.SlugField(unique=True, help_text="Must match a line in routes.py")
    tagline = models.CharField(max_length=260, help_text="The line under the heading in the banner")
    meta_description = models.CharField(max_length=170, blank=True, help_text="For Google. Leave empty to use the tagline.")
    intro = models.TextField(help_text="Overview text. Simple formatting is allowed (see the note below the form).")
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)
   
    class Meta: # type: ignore
        ordering = ["group__order", "order", "id"]

    def __str__(self):
        return self.title

    @property
    def tab_title(self):
        return self.short_title or self.title

    def get_absolute_url(self):
        route = SERVICE_ROUTES.get(self.slug)
        return reverse(route[1]) if route else "#"


class BlockKind(models.TextChoices):
    FEATURE = "feature", "What we do (card)"
    STEP = "step", "Process step"
    DELIVERABLE = "deliverable", "Deliverable (what you receive)"
    AUDIENCE = "audience", "Who it is for"
    SECTION = "section", "In-depth section (long text)"
    FAQ = "faq", "FAQ (title = question, text = answer)"


class ServiceBlock(BaseModel):
    page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name="blocks")
    kind = models.CharField(max_length=12, choices=BlockKind.choices)
    title = models.CharField(max_length=160)
    text = models.TextField(help_text="Simple formatting: blank line = new paragraph, '## ' = sub-heading, '- ' = bullet, "
                                      "'1. ' = numbered, **bold**, [link text](https://...)")
    order = models.PositiveSmallIntegerField(default=0, help_text="Smaller number shows first")
   

    class Meta: # type: ignore
        ordering = ["kind", "order", "id"]

    def __str__(self):
        return f"[{self.get_kind_display()}] {self.title}" # type: ignore