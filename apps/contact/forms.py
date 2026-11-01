import re

from django import forms

from .models import Budget, ContactMessage, CountryCode, Region, Service, Topic


class ContactForm(forms.ModelForm):
    topic = forms.ChoiceField(choices=[("", "Please select"), *Topic.choices])
    region = forms.ChoiceField(choices=[("", "Select region"), *Region.choices])
    country_code = forms.ChoiceField(choices=CountryCode.choices, initial=CountryCode.PK)
    services = forms.MultipleChoiceField(
        choices=Service.choices,
        widget=forms.CheckboxSelectMultiple,
        error_messages={"required": "Choose at least one service."},
    )

    class Meta:
        model = ContactMessage
        fields = [
            "topic", "full_name", "email", "country_code", "phone", "company",
            "company_url", "region", "services", "details",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"type": "tel", "placeholder": "(201) 555-0123", "autocomplete": "tel-national"}),
            "company": forms.TextInput(attrs={"autocomplete": "organization"}),
            "company_url": forms.URLInput(attrs={"placeholder": "https://"}),
            "details": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_phone(self):
        digits = re.sub(r"[\s\-()]", "", self.cleaned_data["phone"])
        if not re.fullmatch(r"\d{6,15}", digits):
            raise forms.ValidationError("Enter a valid phone number.")
        return digits


class ChatForm(ContactForm):
    """Same data as the contact page, plus the optional budget and the page it was sent from."""
    budget = forms.ChoiceField(choices=Budget.choices, required=False)
    consent = forms.BooleanField(error_messages={"required": "Please confirm to continue."})

    class Meta(ContactForm.Meta):
        fields = ContactForm.Meta.fields + ["budget", "page_url"]
        widgets = {
            **ContactForm.Meta.widgets,
            "details": forms.Textarea(attrs={"rows": 5, "maxlength": 2000}),
        }