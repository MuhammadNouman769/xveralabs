from django.db import models


class PartnerApplication(models.Model):
    TYPE_CHOICES = [
        ("investor", "Investor partner"),
        ("referral", "Referral & sales partner"),
        ("reseller", "Reseller"),
        ("marketing", "Marketing & growth partner"),
        ("strategic", "Strategic & corporate partner"),
    ]
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("in_review", "In review"),
        ("agreement", "Agreement stage"),
        ("active", "Active partner"),
        ("declined", "Declined"),
    ]

    partner_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone_code = models.CharField(max_length=8, blank=True)
    phone = models.CharField(max_length=30)
    company = models.CharField(max_length=160, blank=True)
    region = models.CharField(max_length=60)
    module = models.CharField("Investor module", max_length=60, blank=True)
    investment_range = models.CharField(max_length=60, blank=True)
    heard_from = models.CharField(max_length=60, blank=True)
    message = models.TextField(max_length=1500)
    consent = models.BooleanField(default=False)

    # internal use (not shown to the applicant)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "partner application"

    def __str__(self):
        return f"{self.full_name} ({self.get_partner_type_display()})"
