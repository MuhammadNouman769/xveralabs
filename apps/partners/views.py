from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from .content import MODULES, PROGRAMS, TYPE_UI
from .forms import PartnerApplicationForm
from .models import Module, PartnerType

# ---------------------------------------------------------------------
# PARTNER TERMS: change the numbers shown on the site in ONE place.
# Confirm these figures with your lawyer/accountant before publishing.
# ---------------------------------------------------------------------
PARTNER_TERMS = {
    "referral_commission": "5%",   # commission on net revenue of a referred project
    "investor_share": "5%",        # indicative share of a module's net profit (not guaranteed)
}


def _programs():
    out = []
    for p in PROGRAMS:
        item = dict(p)
        item["reward_big"] = PARTNER_TERMS.get(p["reward_key"]) if p.get("reward_key") else ""
        item["reward_word"] = p.get("reward_label", "")
        item["earns"] = p["earns"].format(**PARTNER_TERMS)
        out.append(item)
    return out


class PartnersView(TemplateView):
    template_name = "partners/partners.html"          # adjust to where you put the templates

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(terms=PARTNER_TERMS, programs=_programs())
        return ctx


class InvestorsView(TemplateView):
    template_name = "partners/partners-investors.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(terms=PARTNER_TERMS, modules=MODULES)
        return ctx


# ------------------------------ apply ------------------------------
def _client_ip(request):
    fwd = request.META.get("HTTP_X_FORWARDED_FOR")
    return (fwd.split(",")[0].strip() if fwd else request.META.get("REMOTE_ADDR")) or None


def _throttled(ip, limit=5, window=3600):
    key = f"partner_apply:{ip}"
    cache.add(key, 0, window)
    try:
        return cache.incr(key) > limit
    except ValueError:
        return False


def _notify(app):
    """Email the team and confirm to the applicant. A mail failure must never lose the application."""
    sender = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    team = getattr(settings, "PARTNER_NOTIFY_EMAIL", None)
    if team:
        body = (
            f"Reference: {app.reference}\nType: {app.get_partner_type_display()}\n"
            f"Name: {app.full_name}\nEmail: {app.email}\nPhone: {app.full_phone}\n"
            f"Company: {app.company}\nRegion: {app.get_region_display()}\n"
            f"Module: {app.get_module_display()}\nRange: {app.get_investment_range_display()}\n"
            f"Heard from: {app.get_heard_from_display()}\n\n{app.message}\n"
        )
        send_mail(f"[Xvera Labs] New partner application: {app.full_name} ({app.reference})", body, sender, [team], fail_silently=True)
    send_mail(
        "We received your partner application",
        f"Hello {app.full_name},\n\nThank you for applying to partner with Xvera Labs. "
        f"Your reference is {app.reference}. Our team will review your application and contact you to arrange an intro call.\n\n"
        "Applying does not commit you to anything. Every partnership starts with a written agreement.\n\nXvera Labs",
        sender, [app.email], fail_silently=True,
    )


class ApplyView(View):
    template_name = "partners/partners-apply.html"

    def get(self, request):
        initial = {}
        if request.GET.get("type") in PartnerType.values:
            initial["partner_type"] = request.GET["type"]
        if request.GET.get("module") in Module.values:
            initial["module"] = request.GET["module"]
        form = PartnerApplicationForm(initial=initial, auto_id="pa-%s")
        ref = request.session.pop("partner_ref", "") if request.GET.get("sent") == "1" else ""
        return self._render(request, form, sent=bool(ref) or request.GET.get("sent") == "1", ref=ref)

    def post(self, request):
        if request.POST.get("website"):                       # honeypot: pretend it worked
            return redirect(f"{reverse('partner_apply')}?sent=1")
        ip = _client_ip(request)
        form = PartnerApplicationForm(request.POST, auto_id="pa-%s")
        if _throttled(ip):
            form.add_error(None, "Too many applications from this connection. Please try again later.")
            return self._render(request, form, status=429)
        if form.is_valid():
            app = form.save(commit=False)
            app.ip_address = ip
            app.save()
            _notify(app)
            request.session["partner_ref"] = app.reference
            return redirect(f"{reverse('partner_apply')}?sent=1")
        return self._render(request, form, status=400)

    def _render(self, request, form, status=200, sent=False, ref=""):
        chosen = form["partner_type"].value()
        cards = [
            {"value": t.value, "title": TYPE_UI[t.value][0], "hint": TYPE_UI[t.value][1], "checked": chosen == t.value}
            for t in PartnerType
        ]
        ctx = {"form": form, "type_cards": cards, "is_investor": chosen == PartnerType.INVESTOR, "sent": sent, "ref": ref, "terms": PARTNER_TERMS}
        return render(request, self.template_name, ctx, status=status)