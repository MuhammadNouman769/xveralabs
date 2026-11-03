from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import redirect, render
from django.views import View

from .forms import ApplicationForm
from .models import AppStatus, Application, Cohort, ItemKind, ProgramItem, Story


def _client_ip(request):
    fwd = request.META.get("HTTP_X_FORWARDED_FOR")
    return (fwd.split(",")[0].strip() if fwd else request.META.get("REMOTE_ADDR")) or None


def _throttled(ip, limit=5, window=3600):
    key = f"campus_apply:{ip}"
    cache.add(key, 0, window)
    try:
        return cache.incr(key) > limit
    except ValueError:
        return False


def _notify(app):
    """Email the team and confirm to the applicant. A mail failure must never lose an application."""
    sender = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    team = getattr(settings, "CAMPUS_NOTIFY_EMAIL", None) or getattr(settings, "PARTNER_NOTIFY_EMAIL", None)
    if team:
        body = (f"Reference: {app.reference}\nName: {app.full_name}\nEmail: {app.email}\nPhone: {app.phone}\n"
                f"University: {app.university} ({app.city})\nDegree: {app.degree}, year {app.get_year_of_study_display()}\n"
                f"Profile: {app.social_url}\n\nWhy join:\n{app.motivation}\n\nExperience:\n{app.experience}\n")
        send_mail(f"[Xvera Labs] Ambassador application: {app.full_name} ({app.reference})", body, sender, [team], fail_silently=True)
    send_mail(
        "We received your Campus Ambassador application",
        f"Hello {app.full_name},\n\nThank you for applying to the Xvera Labs Campus Ambassador Program. "
        f"Your reference is {app.reference}. Our team will review your application and contact you.\n\nXvera Labs",
        sender, [app.email], fail_silently=True,
    )


class CampusAmbassadorView(View):
    template_name = "about/campus/campus-ambassador-program.html"      # adjust to where you put the template

    def get(self, request):
        ref = request.session.pop("campus_ref", "") if request.GET.get("sent") == "1" else ""
        return self.render(request, ApplicationForm(auto_id="cp-%s"), sent=request.GET.get("sent") == "1", ref=ref)

    def post(self, request):
        here = request.path
        if request.POST.get("website"):                           # honeypot: pretend it worked
            return redirect(f"{here}?sent=1#apply")
        cohort = Cohort.objects.current() # type: ignore
        form = ApplicationForm(request.POST, auto_id="cp-%s")
        ip = _client_ip(request)
        if cohort is None or not cohort.is_accepting:
            form.add_error(None, "Applications are closed right now.")
            return self.render(request, form, status=400)
        if _throttled(ip):
            form.add_error(None, "Too many applications from this connection. Please try again later.")
            return self.render(request, form, status=429)
        if form.is_valid():
            app = form.save(commit=False)
            app.cohort, app.ip_address = cohort, ip
            app.save()
            _notify(app)
            request.session["campus_ref"] = app.reference
            return redirect(f"{here}?sent=1#apply")
        return self.render(request, form, status=400)

    def render(self, request, form, status=200, sent=False, ref=""):
        items = {}
        for it in ProgramItem.objects.filter(is_active=True):
            items.setdefault(it.kind, []).append(it)
        active = Application.objects.filter(status=AppStatus.ACTIVE)
        n_amb = active.count()
        n_campus = active.values("university").annotate(n=Count("id")).count() if n_amb else 0
        cohort = Cohort.objects.current() # pyright: ignore[reportAttributeAccessIssue]
        ctx = {
            "form": form, "cohort": cohort, "sent": sent, "ref": ref,
            "accepting": bool(cohort and cohort.is_accepting),
            "benefits": items.get(ItemKind.BENEFIT, []), "steps": items.get(ItemKind.STEP, []),
            "responsibilities": items.get(ItemKind.RESPONSIBILITY, []), "faqs": items.get(ItemKind.FAQ, []),
            "stories": Story.objects.filter(is_published=True), # type: ignore
            "ambassadors": n_amb, "campuses": n_campus,
        }
        return render(request, self.template_name, ctx, status=status)