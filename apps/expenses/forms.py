from django import forms
from pathlib import Path

from .models import Expense


class ExpenseForm(forms.ModelForm):
    allowed_receipt_extensions = {".pdf", ".jpg", ".jpeg", ".png", ".webp"}

    class Meta:
        model = Expense
        fields = (
            "title",
            "category",
            "expense_date",
            "vendor",
            "amount",
            "currency",
            "payment_method",
            "status",
            "reference",
            "notes",
            "receipt",
        )
        widgets = {
            "expense_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_receipt(self):
        receipt = self.cleaned_data.get("receipt")
        if not receipt or not hasattr(receipt, "size"):
            return receipt
        if Path(receipt.name).suffix.lower() not in self.allowed_receipt_extensions:
            raise forms.ValidationError("Upload a PDF or image receipt (JPG, PNG, or WebP).")
        if receipt.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Receipt files must be 10 MB or smaller.")
        return receipt
