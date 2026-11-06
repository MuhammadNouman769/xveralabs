import os
import uuid
from apps.utils.models import BaseModel
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from .storage import private_storage


# ---- Dropdown data lives here. Edit once, the pages update themselves. ----
class Department(models.TextChoices):
    ENGINEERING = "engineering", "Engineering"
    CLOUD = "cloud", "Cloud"
    AI = "ai", "AI & ML"
    DEVOPS = "devops", "DevOps"
    PRODUCT = "product", "Product"
    DESIGN = "design", "Design"
    QA = "qa", "Quality assurance"
    MARKETING = "marketing", "Marketing & sales"
    OPERATIONS = "operations", "Operations"


class JobType(models.TextChoices):
    FULL_TIME = "full_time", "Full-time"
    PART_TIME = "part_time", "Part-time"
    CONTRACT = "contract", "Contract"
    INTERNSHIP = "internship", "Internship"


class WorkMode(models.TextChoices):
    REMOTE = "remote", "Remote"
    HYBRID = "hybrid", "Hybrid"
    ONSITE = "onsite", "On-site"


class Level(models.TextChoices):
    INTERN = "intern", "Intern"
    ENTRY = "entry", "Entry level"
    MID = "mid", "Mid level"
    SENIOR = "senior", "Senior"
    LEAD = "lead", "Lead"


class AppStatus(models.TextChoices):
    NEW = "new", "New"
    REVIEWING = "reviewing", "Reviewing"
    SHORTLISTED = "shortlisted", "Shortlisted"
    INTERVIEW = "interview", "Interview"
    OFFER = "offer", "Offer"
    HIRED = "hired", "Hired"
    REJECTED = "rejected", "Not selected"


class JobQuerySet(models.QuerySet):
    def open(self):
        """Positions that are switched on and not past their deadline."""
        return self.filter(is_open=True).filter(
            models.Q(deadline__isnull=True) | models.Q(deadline__gte=timezone.localdate())
        )


def _lines(text):
    return [ln.strip(" \t-\u2022*") for ln in text.splitlines() if ln.strip(" \t-\u2022*")]


class JobPosition(BaseModel):
    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    department = models.CharField(max_length=20, choices=Department.choices)
    job_type = models.CharField("Type", max_length=20, choices=JobType.choices, default=JobType.FULL_TIME)
    work_mode = models.CharField(max_length=10, choices=WorkMode.choices, default=WorkMode.REMOTE)
    level = models.CharField(max_length=10, choices=Level.choices, default=Level.MID)
    location = models.CharField(max_length=120, default="Lahore, Pakistan")
    duration = models.CharField(max_length=60, blank=True, help_text="For internships and contracts, e.g. 3 months")
    compensation = models.CharField(max_length=120, blank=True, help_text="Only fill this if you want to show it, e.g. Paid stipend")
    summary = models.CharField(max_length=240, help_text="One or two lines shown on the list")
    description = models.TextField(help_text="About the role. Blank line = new paragraph.")
    responsibilities = models.TextField(blank=True, help_text="One item per line")
    requirements = models.TextField(blank=True, help_text="One item per line")
    nice_to_have = models.TextField(blank=True, help_text="One item per line")

    is_open = models.BooleanField(default=True, help_text="Untick to close the position")
    is_featured = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True, help_text="Optional. The position closes automatically after this date.")
 
    objects = JobQuerySet.as_manager()

    class Meta: # type: ignore
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_job_type_display()})" # type: ignore

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:150] or "position"
            slug, n = base, 2
            while JobPosition.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("career_detail", args=[self.slug])

    @property
    def is_internship(self):
        return self.job_type == JobType.INTERNSHIP

    @property
    def is_accepting(self):
        return self.is_open and (self.deadline is None or self.deadline >= timezone.localdate())

    @property
    def paragraphs(self):
        return [p.strip() for p in self.description.split("\n\n") if p.strip()]

    @property
    def responsibilities_list(self):
        return _lines(self.responsibilities)

    @property
    def requirements_list(self):
        return _lines(self.requirements)

    @property
    def nice_to_have_list(self):
        return _lines(self.nice_to_have)


def cv_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f"cvs/{timezone.now():%Y/%m}/{uuid.uuid4().hex}{ext}"


class JobApplication(BaseModel):
    position = models.ForeignKey(JobPosition, null=True, blank=True, on_delete=models.SET_NULL, related_name="applications")
    position_title = models.CharField(max_length=140, blank=True, help_text="Kept even if the position is later deleted")
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=80, blank=True)
    profile_url = models.URLField("LinkedIn / GitHub / portfolio", blank=True)
    cover_note = models.TextField(max_length=1500, blank=True)
    cv = models.FileField(upload_to=cv_path, storage=private_storage)
    consent = models.BooleanField(default=False)

    # internal use (never shown to the applicant)
    status = models.CharField(max_length=15, choices=AppStatus.choices, default=AppStatus.NEW, db_index=True)
    internal_notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
  
    class Meta: # type: ignore
        ordering = ["-created_at"]
        verbose_name = "job application"

    def __str__(self):
        return f"{self.full_name} - {self.position_title or 'General application'}"

    @property
    def reference(self):
        return f"CA-{self.pk:05d}"