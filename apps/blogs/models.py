from django.db import models


class Resource(models.Model):
    class Topic(models.TextChoices):
        TECHNOLOGY = "technology", "Technology"
        BUSINESS = "business", "Business"
        INDUSTRY = "industry", "Industry"

    class Kind(models.TextChoices):
        ARTICLE = "article", "Article"
        GUIDE = "guide", "Guide"
        REPORT = "report", "Report"

    slug = models.SlugField(max_length=180, unique=True)
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=100)
    topic = models.CharField(max_length=20, choices=Topic.choices)
    kind = models.CharField(max_length=12, choices=Kind.choices)
    read_time = models.CharField(max_length=40)
    excerpt = models.TextField()
    image = models.URLField(max_length=500)
    image_alt = models.CharField(max_length=240)
    sections = models.JSONField(default=list, help_text="JSON list: heading, paragraphs and bullets.")
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def as_catalog_entry(self):
        return {
            "slug": self.slug,
            "title": self.title,
            "category": self.category,
            "topic": self.topic,
            "kind": self.kind,
            "read_time": self.read_time,
            "excerpt": self.excerpt,
            "image": self.image,
            "image_alt": self.image_alt,
            "sections": self.sections,
        }
