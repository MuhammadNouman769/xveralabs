from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import PartnerApplicationForm

# ---------------------------------------------------------------------
# PARTNER TERMS: change the numbers shown on the site in ONE place.
# These are the figures you chose; confirm them with your lawyer/accountant.
# ---------------------------------------------------------------------
PARTNER_TERMS = {
    "referral_commission": "5%",   # commission on net revenue of a referred project
    "investor_share": "5%",        # indicative share of a module's net profit (not guaranteed)
}


class PartnersView(TemplateView):
    template_name = "partners/partners.html"          # adjust to where you put the templates

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["terms"] = PARTNER_TERMS
        return ctx


class InvestorsView(TemplateView):
    template_name = "partners/partners-investors.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["terms"] = PARTNER_TERMS
        return ctx


def partner_apply(request):
    if request.method == "POST":
        form = PartnerApplicationForm(request.POST)
        if form.is_valid():
            if form.is_spam():
                # pretend it worked so bots learn nothing
                messages.success(request, "Thank you. Your application has been received.")
                return redirect("partner_apply")

            application = form.save()

            # email notification (set EMAIL_* and PARTNER_NOTIFY_EMAIL in settings.py)
            notify_to = getattr(settings, "PARTNER_NOTIFY_EMAIL", None)
            if notify_to:
                body = (
                    f"Type: {application.get_partner_type_display()}\n"
                    f"Name: {application.full_name}\n"
                    f"Email: {application.email}\n"
                    f"Phone: {application.phone_code} {application.phone}\n"
                    f"Company: {application.company}\n"
                    f"Region: {application.region}\n"
                    f"Module: {application.module}\n"
                    f"Range: {application.investment_range}\n\n"
                    f"{application.message}"
                )
                send_mail(
                    subject=f"New partner application: {application.full_name}",
                    message=body,
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=[notify_to],
                    fail_silently=True,
                )

            messages.success(request, "Thank you. Your application has been received and our team will be in touch.")
            return redirect("partner_apply")

        messages.error(request, "Please check the form and try again.")
        return redirect("partner_apply")

    return render(request, "partners/partners-apply.html", {"terms": PARTNER_TERMS})
