from django import forms

from .models import PartnerApplication


class PartnerApplicationForm(forms.ModelForm):
    # spam trap: the template hides this field from real users
    website = forms.CharField(required=False)

    class Meta:
        model = PartnerApplication
        fields = [
            "partner_type", "full_name", "email", "phone_code", "phone",
            "company", "region", "module", "investment_range", "heard_from",
            "message", "consent",
        ]

    def clean_consent(self):
        if not self.cleaned_data.get("consent"):
            raise forms.ValidationError("Consent is required.")
        return True

    def is_spam(self):
        return bool(self.cleaned_data.get("website"))
