from django.db import models
from django.utils import timezone
from django.utils.text import slugify

""" ========= Base Model =========== """

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


""" ========= Form submissions (contact, partner, job, ambassador) =========== """

class SubmissionModel(BaseModel):
    """Base for everything a visitor sends us through a form.

    Gives you everything from BaseModel (is_active, created_at, updated_at) plus
    ip_address, internal_notes, newest-first ordering and a reference number such as PA-00012.

    Each child sets its own reference_prefix and its own `status` field (the choices differ per app):

        class PartnerApplication(SubmissionModel):
            reference_prefix = "PA"
            status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, db_index=True)

        class Meta(SubmissionModel.Meta):
            verbose_name = "partner application"
    """
    reference_prefix = "REF"

    internal_notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        abstract = True
        ordering = ["-created_at"]

    @property
    def reference(self):
        return f"{self.reference_prefix}-{self.pk:05d}" if self.pk else ""


""" ========= Person who contacts us =========== """

class ContactPersonModel(models.Model):
    """The usual three contact fields. Handy for new forms."""
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    class Meta:
        abstract = True


""" ========= Ordering and publishing =========== """

class OrderedModel(models.Model):
    """Lets staff choose the order in the admin (smaller number shows first)."""
    order = models.PositiveSmallIntegerField(default=0, help_text="Smaller number shows first")

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PublishableModel(models.Model):
    """Draft / published switch. On the pages use Model.objects.published()."""
    is_published = models.BooleanField(default=True)

    objects = PublishedQuerySet.as_manager()

    class Meta:
        abstract = True


""" ========= Slug =========== """

class SlugModel(models.Model):
    """Fills `slug` automatically from another field (default: title) and keeps it unique.

        class Post(SlugModel):
            slug_source = "title"
            title = models.CharField(max_length=140)
    """
    slug_source = "title"
    slug = models.SlugField(max_length=160, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(getattr(self, self.slug_source, ""))[:150] or "item"
            slug, n = base, 2
            while type(self).objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        super().save(*args, **kwargs)


""" ========= Open / closed with an optional date =========== """

class OpenUntilModel(models.Model):
    """For things that can be switched off or expire: job positions, cohorts, offers.
    `is_accepting` is True when it is switched on and the deadline has not passed."""
    is_open = models.BooleanField(default=True)
    deadline = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def is_accepting(self):
        return self.is_open and (self.deadline is None or self.deadline >= timezone.localdate())