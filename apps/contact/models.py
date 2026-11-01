from django.db import models


# ---- Dropdown / checkbox data lives here. Edit once, the form updates itself. ----
class Topic(models.TextChoices):
    NEW_PROJECT = "new_project", "A new project"
    PARTNERSHIP = "partnership", "Partnership or investment"
    CAREERS = "careers", "Careers"
    OTHER = "other", "Something else"


class Region(models.TextChoices):
    PAKISTAN = "pakistan", "Pakistan"
    MIDDLE_EAST = "middle_east", "Middle East"
    NORTH_AMERICA = "north_america", "North America"
    EUROPE = "europe", "Europe"
    ASIA_PACIFIC = "asia_pacific", "Asia Pacific"
    OTHER = "other", "Other"


class Service(models.TextChoices):
    REMOTE_IT = "remote-it", "Remote IT resources"
    CUSTOM_SOFTWARE = "custom-software", "Custom software"
    WEB = "web", "Web development"
    MOBILE = "mobile", "Mobile apps"
    AR_VR = "ar-vr", "AR/VR"
    GAMING = "gaming", "Gaming"
    CYBER = "cyber-security", "Cyber security"
    OTHER = "other", "Other IT services"


class CountryCode(models.TextChoices):
    PK = "+92", "🇵🇰 +92"
    US = "+1", "🇺🇸 +1"
    UK = "+44", "🇬🇧 +44"
    AE = "+971", "🇦🇪 +971"
    SA = "+966", "🇸🇦 +966"
    AU = "+61", "🇦🇺 +61"
    DE = "+49", "🇩🇪 +49"


class Budget(models.TextChoices):
    LT_50K = "lt-50k", "Less than PKR 50,000"
    B_50_100 = "50-100k", "PKR 50,000 - 100,000"
    B_100_150 = "100-150k", "PKR 100,000 - 150,000"
    B_150_200 = "150-200k", "PKR 150,000 - 200,000"
    B_200_250 = "200-250k", "PKR 200,000 - 250,000"
    B_250_300 = "250-300k", "PKR 250,000 - 300,000"
    B_300_350 = "300-350k", "PKR 300,000 - 350,000"
    B_350_400 = "350-400k", "PKR 350,000 - 400,000"
    B_400_500 = "400-500k", "PKR 400,000 - 500,000"
    GT_500K = "gt-500k", "More than PKR 500,000"
    NOT_SURE = "not-sure", "Not sure yet"


class Source(models.TextChoices):
    PAGE = "page", "Contact page"
    CHAT = "chat", "Chat sidebar"


class Status(models.TextChoices):
    NEW = "new", "New"
    CONTACTED = "contacted", "Contacted"
    CLOSED = "closed", "Closed"


class ContactMessage(models.Model):
    topic = models.CharField(max_length=20, choices=Topic.choices)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    country_code = models.CharField(max_length=6, choices=CountryCode.choices, default=CountryCode.PK)
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=150)
    company_url = models.URLField(blank=True)
    region = models.CharField(max_length=20, choices=Region.choices)
    services = models.JSONField(default=list)
    details = models.TextField()
    budget = models.CharField(max_length=10, choices=Budget.choices, blank=True)
    source = models.CharField(max_length=10, choices=Source.choices, default=Source.PAGE)
    page_url = models.CharField(max_length=500, blank=True)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NEW, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "contact message"

    def __str__(self):
        return f"{self.full_name} ({self.company}) - {self.get_topic_display()}" # type: ignore

    @property
    def full_phone(self):
        return f"{self.country_code}{self.phone}"

    @property
    def service_labels(self):
        names = dict(Service.choices)
        return [names.get(s, s) for s in self.services]