from django.db import models
from apps.utils.models import BaseModel

# ---- Dropdown data lives here. Edit once, the apply form updates itself. ----
class PartnerType(models.TextChoices):
    REFERRAL = "referral", "Referral & sales partner"
    RESELLER = "reseller", "Reseller"
    MARKETING = "marketing", "Marketing & growth partner"
    STRATEGIC = "strategic", "Strategic & corporate partner"
    INVESTOR = "investor", "Investor partner"


class Status(models.TextChoices):
    NEW = "new", "New"
    CONTACTED = "contacted", "Contacted"
    IN_REVIEW = "in_review", "In review"
    AGREEMENT = "agreement", "Agreement stage"
    ACTIVE = "active", "Active partner"
    DECLINED = "declined", "Declined"


class Region(models.TextChoices):
    PAKISTAN = "Pakistan", "Pakistan"
    MIDDLE_EAST = "Middle East", "Middle East"
    EUROPE = "Europe", "Europe"
    NORTH_AMERICA = "North America", "North America"
    ASIA_PACIFIC = "Asia Pacific", "Asia Pacific"
    AFRICA = "Africa", "Africa"
    OTHER = "Other", "Other"


class Module(models.TextChoices):
    BTR_MALL = "btr-mall", "BTR Mall"
    DINEX_POS = "dinex-pos", "Dinex POS"
    SKILLS_ACADEMY = "skills-academy", "Xvera Skills Academy"
    OTHER = "other", "Other ventures"


class InvestmentRange(models.TextChoices):
    UNDER_500K = "under-500k", "Under PKR 500,000"
    R_500K_2M = "500k-2m", "PKR 500,000 to 2,000,000"
    R_2M_10M = "2m-10m", "PKR 2,000,000 to 10,000,000"
    OVER_10M = "over-10m", "Above PKR 10,000,000"


class HeardFrom(models.TextChoices):
    SEARCH = "search", "Search engine"
    SOCIAL = "social", "Social media"
    FRIEND = "friend", "Friend or colleague"
    EVENT = "event", "Event"
    OTHER = "other", "Other"


class PhoneCode(models.TextChoices):
    PK = "+92", "🇵🇰 +92"
    US = "+1", "🇺🇸 +1"
    UK = "+44", "🇬🇧 +44"
    AE = "+971", "🇦🇪 +971"
    SA = "+966", "🇸🇦 +966"
    AU = "+61", "🇦🇺 +61"
    DE = "+49", "🇩🇪 +49"


class PartnerApplication(BaseModel):
    partner_type = models.CharField(max_length=20, choices=PartnerType.choices, db_index=True)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_code = models.CharField(max_length=8, blank=True, choices=PhoneCode.choices)
    phone = models.CharField(max_length=30)
    company = models.CharField(max_length=160, blank=True)
    region = models.CharField(max_length=60, choices=Region.choices)
    module = models.CharField("Investor module", max_length=60, blank=True, choices=Module.choices)
    investment_range = models.CharField(max_length=60, blank=True, choices=InvestmentRange.choices)
    heard_from = models.CharField(max_length=60, blank=True, choices=HeardFrom.choices)
    message = models.TextField(max_length=1500)
    consent = models.BooleanField(default=False)

    # internal use (never shown to the applicant)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW, db_index=True)
    internal_notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: # type: ignore
        ordering = ["-created_at"]
        verbose_name = "partner application"

    def __str__(self):
        return f"{self.full_name} ({self.get_partner_type_display()})" # type: ignore

    @property
    def reference(self):
        return f"PA-{self.pk:05d}"

    @property
    def full_phone(self):
        return f"{self.phone_code}{self.phone}"