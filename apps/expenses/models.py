from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from .storage import private_expense_storage


class Expense(models.Model):
    class Category(models.TextChoices):
        SALARIES = "salaries", "Salaries & contractors"
        SOFTWARE = "software", "Software & subscriptions"
        MARKETING = "marketing", "Marketing"
        TRAVEL = "travel", "Travel & transport"
        RENT = "rent", "Rent & facilities"
        UTILITIES = "utilities", "Utilities"
        EQUIPMENT = "equipment", "Equipment & hardware"
        PROFESSIONAL = "professional", "Professional services"
        OFFICE = "office", "Office supplies"
        OTHER = "other", "Other"

    class Currency(models.TextChoices):
        PKR = "PKR", "PKR — Pakistani Rupee"
        USD = "USD", "USD — US Dollar"
        AED = "AED", "AED — UAE Dirham"
        GBP = "GBP", "GBP — Pound Sterling"
        EUR = "EUR", "EUR — Euro"
        SAR = "SAR", "SAR — Saudi Riyal"
        CAD = "CAD", "CAD — Canadian Dollar"
        AUD = "AUD", "AUD — Australian Dollar"

    class PaymentMethod(models.TextChoices):
        BANK = "bank", "Bank transfer"
        CARD = "card", "Company card"
        CASH = "cash", "Cash"
        WALLET = "wallet", "Mobile wallet"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        PAID = "paid", "Paid"
        PENDING = "pending", "Pending"

    title = models.CharField(max_length=160)
    category = models.CharField(max_length=20, choices=Category.choices)
    expense_date = models.DateField(db_index=True)
    vendor = models.CharField(max_length=160, blank=True)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.PKR,
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.BANK,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PAID,
        db_index=True,
    )
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    receipt = models.FileField(
        upload_to="receipts/%Y/%m/",
        storage=private_expense_storage,
        blank=True,
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="recorded_expenses",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-expense_date", "-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="expense_amount_must_be_positive",
            )
        ]

    def __str__(self):
        return f"{self.title} — {self.amount} {self.currency}"
