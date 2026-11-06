from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models, transaction

from .storage import private_expense_storage


class ReferenceTrackedModel(models.Model):
    reference = models.CharField(max_length=100, blank=True)
    reference_prefix = None

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        with transaction.atomic():
            result = super().save(*args, **kwargs)
            if not self.reference:
                reference = f"{self.reference_prefix}-{self.pk:06d}"
                suffix = 2
                while type(self).objects.filter(reference=reference).exclude(pk=self.pk).exists():
                    reference = f"{self.reference_prefix}-{self.pk:06d}-{suffix}"
                    suffix += 1
                type(self).objects.filter(pk=self.pk).update(reference=reference)
                self.reference = reference
            return result


class Expense(ReferenceTrackedModel):
    reference_prefix = "EXP"

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


class CompanyIncome(ReferenceTrackedModel):
    reference_prefix = "INC"

    class Status(models.TextChoices):
        RECEIVED = "received", "Received"
        PENDING = "pending", "Pending"

    title = models.CharField(max_length=160)
    source = models.CharField(max_length=120)
    income_date = models.DateField(db_index=True)
    payer = models.CharField(max_length=160, blank=True)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    currency = models.CharField(
        max_length=3,
        choices=Expense.Currency.choices,
        default=Expense.Currency.PKR,
    )
    payment_method = models.CharField(
        max_length=10,
        choices=Expense.PaymentMethod.choices,
        default=Expense.PaymentMethod.BANK,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.RECEIVED,
        db_index=True,
    )
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="recorded_company_incomes",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-income_date", "-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="company_income_amount_must_be_positive",
            )
        ]

    def __str__(self):
        return f"{self.title} — {self.amount} {self.currency}"
