import re

from django import forms

from .models import Application, YearOfStudy


class ApplicationForm(forms.ModelForm):
    year_of_study = forms.ChoiceField(choices=[("", "Select year"), *YearOfStudy.choices])
    is_student = forms.BooleanField(error_messages={"required": "Only currently enrolled students can apply."})
    consent = forms.BooleanField(error_messages={"required": "Please confirm to continue."})

    class Meta:
        model = Application
        fields = ["full_name", "email", "phone", "university", "city", "degree", "year_of_study",
                  "motivation", "experience", "social_url", "is_student", "consent"]
        widgets = {
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"type": "tel", "autocomplete": "tel", "placeholder": "+92 300 1234567"}),
            "university": forms.TextInput(attrs={"autocomplete": "organization"}),
            "city": forms.TextInput(attrs={"autocomplete": "address-level2"}),
            "degree": forms.TextInput(attrs={"placeholder": "e.g. BS Computer Science"}),
            "motivation": forms.Textarea(attrs={"rows": 5, "maxlength": 1000, "placeholder": "Tell us why you want to represent Xvera Labs on your campus"}),
            "experience": forms.Textarea(attrs={"rows": 4, "maxlength": 1000, "placeholder": "Societies, events, communities or projects you have led or helped with (optional)"}),
            "social_url": forms.URLInput(attrs={"placeholder": "https://"}),
        }

    def clean_phone(self):
        digits = re.sub(r"[\s\-()+]", "", self.cleaned_data["phone"])
        if not re.fullmatch(r"\d{7,15}", digits):
            raise forms.ValidationError("Enter a valid phone number.")
        return self.cleaned_data["phone"].strip()

    def clean_motivation(self):
        m = self.cleaned_data["motivation"].strip()
        if len(m) < 30:
            raise forms.ValidationError("Please write a little more (at least 30 characters).")
        return m