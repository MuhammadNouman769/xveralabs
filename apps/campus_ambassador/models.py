from django.db import models
from django.utils import timezone
from apps.utils.models import BaseModel


class YearOfStudy(models.TextChoices):
    Y1 = "1", "1st year"
    Y2 = "2", "2nd year"
    Y3 = "3", "3rd year"
    Y4 = "4", "4th year"
    Y5 = "5", "5th year or above"
    GRAD = "grad", "Postgraduate"


class AppStatus(models.TextChoices):
    NEW = "new", "New"
    REVIEWING = "reviewing", "Reviewing"
    INTERVIEW = "interview", "Interview"
    SELECTED = "selected", "Selected"
    ACTIVE = "active", "Active ambassador"
    REJECTED = "rejected", "Not selected"
    WITHDRAWN = "withdrawn", "Withdrawn"


class ItemKind(models.TextChoices):
    BENEFIT = "benefit", "Benefit"
    STEP = "step", "How it works step"
    RESPONSIBILITY = "responsibility", "Responsibility"
    FAQ = "faq", "FAQ (title = question, text = answer)"


class CohortQuerySet(models.QuerySet):
    def current(self):
        """The cohort the page should show: the newest one that is accepting, else the newest one."""
        for c in self.order_by("-created_at"):
            if c.is_accepting:
                return c
        return self.order_by("-created_at").first()


class Cohort(BaseModel):
    name = models.CharField(max_length=80, help_text="e.g. Spring 2027 cohort")
    is_open = models.BooleanField(default=True, help_text="Untick to close applications")
    opens_on = models.DateField(null=True, blank=True)
    closes_on = models.DateField(null=True, blank=True, help_text="Last day to apply (optional)")
    term_months = models.PositiveSmallIntegerField(default=3, help_text="How long the program runs")
    hours_per_week = models.CharField(max_length=40, blank=True, help_text="e.g. 4 to 6 hours")
    eligibility = models.TextField(blank=True, help_text="Who can apply. One point per line.")
   
    objects = CohortQuerySet.as_manager()

    class Meta: # type: ignore
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def is_accepting(self):
        today = timezone.localdate()
        return (self.is_open
                and (self.opens_on is None or self.opens_on <= today)
                and (self.closes_on is None or self.closes_on >= today))

    @property
    def eligibility_list(self):
        return [ln.strip(" \t-\u2022*") for ln in self.eligibility.splitlines() if ln.strip(" \t-\u2022*")]


class ProgramItem(models.Model):
    """Benefits, steps, responsibilities and FAQs shown on the page. Edit them in the dashboard."""
    kind = models.CharField(max_length=15, choices=ItemKind.choices, db_index=True)
    title = models.CharField(max_length=160)
    text = models.TextField()
    order = models.PositiveSmallIntegerField(default=0, help_text="Smaller number shows first")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["kind", "order", "id"]

    def __str__(self):
        return f"[{self.get_kind_display()}] {self.title}" # type: ignore


class Story(BaseModel):
    """Real quotes from real ambassadors. The section only appears when at least one is published."""
    name = models.CharField(max_length=80)
    university = models.CharField(max_length=120)
    label = models.CharField(max_length=60, blank=True, help_text="e.g. Spring 2027 cohort")
    quote = models.TextField(max_length=500)
    is_published = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta: # type: ignore
        ordering = ["order", "id"]
        verbose_name_plural = "stories"

    def __str__(self):
        return f"{self.name} ({self.university})"


class Application(BaseModel):
    cohort = models.ForeignKey(Cohort, null=True, blank=True, on_delete=models.SET_NULL, related_name="applications")
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    university = models.CharField("University / college", max_length=160)
    city = models.CharField(max_length=80)
    degree = models.CharField("Degree program", max_length=120)
    year_of_study = models.CharField(max_length=5, choices=YearOfStudy.choices)
    motivation = models.TextField("Why do you want to join?", max_length=1000)
    experience = models.TextField("Leadership / event / community experience", max_length=1000, blank=True)
    social_url = models.URLField("LinkedIn or Instagram link", blank=True)
    is_student = models.BooleanField(default=False)
    consent = models.BooleanField(default=False)

    # internal use (never shown to the applicant)
    status = models.CharField(max_length=12, choices=AppStatus.choices, default=AppStatus.NEW, db_index=True)
    internal_notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
   

    class Meta: # type: ignore
        ordering = ["-created_at"]
        verbose_name = "ambassador application"

    def __str__(self):
        return f"{self.full_name} ({self.university})"

    @property
    def reference(self):
        return f"CAP-{self.pk:05d}"