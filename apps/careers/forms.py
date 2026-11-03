import os
import re

from django import forms

from .models import JobApplication

MAX_CV_MB = 5
ALLOWED_EXT = {".pdf", ".doc", ".docx"}


class ApplicationForm(forms.ModelForm):
    consent = forms.BooleanField(error_messages={"required": "Please confirm to continue."})

    class Meta:
        model = JobApplication
        fields = ["full_name", "email", "phone", "city", "profile_url", "cover_note", "cv", "consent"]
        widgets = {
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"type": "tel", "autocomplete": "tel", "placeholder": "+92 300 1234567"}),
            "city": forms.TextInput(attrs={"autocomplete": "address-level2"}),
            "profile_url": forms.URLInput(attrs={"placeholder": "https://"}),
            "cover_note": forms.Textarea(attrs={"rows": 5, "maxlength": 1500, "placeholder": "A few lines about you and why this role interests you (optional)"}),
            "cv": forms.ClearableFileInput(attrs={"accept": ".pdf,.doc,.docx"}),
        }
        error_messages = {"cv": {"required": "Please attach your CV."}}

    def clean_phone(self):
        digits = re.sub(r"[\s\-()+]", "", self.cleaned_data["phone"])
        if not re.fullmatch(r"\d{7,15}", digits):
            raise forms.ValidationError("Enter a valid phone number.")
        return self.cleaned_data["phone"].strip()

    def clean_cv(self):
        f = self.cleaned_data["cv"]
        if os.path.splitext(f.name)[1].lower() not in ALLOWED_EXT:
            raise forms.ValidationError("Please upload a PDF, DOC or DOCX file.")
        if f.size > MAX_CV_MB * 1024 * 1024:
            raise forms.ValidationError(f"The file is too large. Maximum size is {MAX_CV_MB} MB.")
        return f