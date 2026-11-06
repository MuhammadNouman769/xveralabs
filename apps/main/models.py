from django.db import models

# Create your models here.
from django.db import models

from apps.utils.models import BaseModel


class IndustryCaseStudy(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    eyebrow = models.CharField(max_length=100)
    title = models.CharField(max_length=180)
    summary = models.TextField()
    image_url = models.URLField(max_length=500)
    image_alt = models.CharField(max_length=180)
    challenge = models.TextField()
    approach = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):  # type: ignore
        ordering = ["order", "name"]
        verbose_name = "industry case study"
        verbose_name_plural = "industry case studies"

    def __str__(self):
        return self.name


class IndustryCaseStudyBlock(BaseModel):
    class Kind(models.TextChoices):
        CAPABILITY = "capability", "Capability"
        CONSIDERATION = "consideration", "Consideration"

    case_study = models.ForeignKey(
        IndustryCaseStudy,
        on_delete=models.CASCADE,
        related_name="blocks",
    )
    kind = models.CharField(max_length=16, choices=Kind.choices)
    title = models.CharField(max_length=160)
    text = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta(BaseModel.Meta):  # type: ignore
        ordering = ["kind", "order", "id"]

    def __str__(self):
        return f"{self.get_kind_display()}: {self.title}"
