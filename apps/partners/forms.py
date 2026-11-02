import re

from django import forms

from .models import (HeardFrom, InvestmentRange, Module, PartnerApplication,
                     PartnerType, PhoneCode, Region)


class PartnerApplicationForm(forms.ModelForm):
    partner_type = forms.ChoiceField(
        choices=PartnerType.choices,
        error_messages={"required": "Please choose how you would like to partner."},
    )
    phone_code = forms.ChoiceField(choices=PhoneCode.choices, initial=PhoneCode.PK)
    region = forms.ChoiceField(choices=[("", "Select region"), *Region.choices])
    module = forms.ChoiceField(choices=[("", "Not sure yet"), *Module.choices], required=False)
    investment_range = forms.ChoiceField(choices=[("", "Prefer to discuss"), *InvestmentRange.choices], required=False)
    heard_from = forms.ChoiceField(choices=[("", "Select"), *HeardFrom.choices], required=False)
    consent = forms.BooleanField(error_messages={"required": "Please confirm to continue."})

    class Meta:
        model = PartnerApplication
        fields = [
            "partner_type", "full_name", "email", "phone_code", "phone", "company", "region",
            "module", "investment_range", "heard_from", "message", "consent",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"type": "tel", "placeholder": "300 1234567", "autocomplete": "tel-national"}),
            "company": forms.TextInput(attrs={"autocomplete": "organization"}),
            "message": forms.Textarea(attrs={
                "rows": 5, "maxlength": 1500,
                "placeholder": "Who you are, what you do, and how you would like to work with us...",
            }),
        }

    def clean_phone(self):
        digits = re.sub(r"[\s\-()]", "", self.cleaned_data["phone"])
        if not re.fullmatch(r"\d{6,15}", digits):
            raise forms.ValidationError("Enter a valid phone number.")
        return digits

    def clean_message(self):
        msg = self.cleaned_data["message"].strip()
        if len(msg) < 10:
            raise forms.ValidationError("Please add a few details (at least 10 characters).")
        return msg

    def clean(self):
        data = super().clean()
        if data.get("partner_type") != PartnerType.INVESTOR:   # investor-only fields
            data["module"] = ""
            data["investment_range"] = ""
        return data