import json
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.views import View

from .content import BENEFITS, INTERNSHIP_POINTS, PROCESS, VALUES
from .forms import ApplicationForm
from .models import Department, JobApplication, JobPosition, JobType


# ------------------------------ list ------------------------------
class CareersView(View):
    template_name = "about/careers/careers.html"          # adjust to where you put the templates

    def get(self, request):
        positions = list(JobPosition.objects.open()) # type: ignore
        used_depts = {p.department for p in positions}
        used_types = {p.job_type for p in positions}
        ctx = {
            "positions": positions,
            "latest": positions[:4],
            "open_count": len(positions),
            "internship_count": sum(1 for p in positions if p.is_internship),
            "departments": [(v, l) for v, l in Department.choices if v in used_depts],
            "types": [(v, l) for v, l in JobType.choices if v in used_types],
            "values": VALUES, "benefits": BENEFITS, "process": PROCESS, "internship_points": INTERNSHIP_POINTS,
        }
        return render(request, self.template_name, ctx)


# ------------------------------ apply ------------------------------
def _client_ip(request):
    fwd = request.META.get("HTTP_X_FORWARDED_FOR")
    return (fwd.split(",")[0].strip() if fwd else request.META.get("REMOTE_ADDR")) or None


def _throttled(ip, limit=5, window=3600):
    key = f"career_apply:{ip}"
    cache.add(key, 0, window)
    try:
        return cache.incr(key) > limit
    except ValueError:
        return False


def _notify(app):
    """Email HR and confirm to the applicant. A mail failure must never lose an application."""
    sender = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    hr = getattr(settings, "CAREERS_NOTIFY_EMAIL", None)
    role = app.position_title or "General application"
    if hr:
        body = (f"Reference: {app.reference}\nRole: {role}\nName: {app.full_name}\nEmail: {app.email}\n"
                f"Phone: {app.phone}\nCity: {app.city}\nProfile: {app.profile_url}\n\n{app.cover_note}\n\n"
                "The CV is available in the staff dashboard (Job applications).")
        send_mail(f"[Xvera Labs] New application: {app.full_name} - {role} ({app.reference})", body, sender, [hr], fail_silently=True)
    send_mail(
        "We received your application",
        f"Hello {app.full_name},\n\nThank you for applying to Xvera Labs for: {role}.\nYour reference is {app.reference}. "
        "Our team will review your application and contact you if there is a fit.\n\nXvera Labs",
        sender, [app.email], fail_silently=True,
    )


class ApplyBase(View):
    """GET shows the form, POST saves the application. Subclasses set the template and the position."""
    template_name = ""

    def get_position(self, request, **kwargs) -> "JobPosition | None":
        return None

    def extra_context(self, request, position):
        return {}

    def get(self, request, **kwargs):
        position = self.get_position(request, **kwargs)
        ref = request.session.pop("career_ref", "") if request.GET.get("sent") == "1" else ""
        return self.render(request, position, ApplicationForm(auto_id="ca-%s"), sent=request.GET.get("sent") == "1", ref=ref)

    def post(self, request, **kwargs):
        position = self.get_position(request, **kwargs)
        here = request.path
        if request.POST.get("website"):                       # honeypot: pretend it worked
            return redirect(f"{here}?sent=1")
        form = ApplicationForm(request.POST, request.FILES, auto_id="ca-%s")
        ip = _client_ip(request)
        if _throttled(ip):
            form.add_error(None, "Too many applications from this connection. Please try again later.")
            return self.render(request, position, form, status=429)
        if position is not None and not position.is_accepting:
            form.add_error(None, "This position is no longer open.")
            return self.render(request, position, form, status=400)
        if form.is_valid():
            app = form.save(commit=False)
            app.position, app.ip_address = position, ip
            app.position_title = position.title if position else ""
            app.save()
            _notify(app)
            request.session["career_ref"] = app.reference
            return redirect(f"{here}?sent=1#apply")
        return self.render(request, position, form, status=400)

    def render(self, request, position, form, status=200, sent=False, ref=""):
        ctx = {"form": form, "position": position, "sent": sent, "ref": ref}
        ctx.update(self.extra_context(request, position))
        return render(request, self.template_name, ctx, status=status)


class GeneralApplyView(ApplyBase):
    template_name = "about/careers/apply.html"


class PositionView(ApplyBase):
    template_name = "about/careers/career_detail.html"

    def get_position(self, request, **kwargs) -> "JobPosition | None":
        return get_object_or_404(JobPosition, slug=kwargs["slug"])

    def extra_context(self, request, position):
        ld = None
        if position.is_accepting:
            data = {
                "@context": "https://schema.org", "@type": "JobPosting", "title": position.title,
                "description": " ".join([position.summary] + position.paragraphs),
                "datePosted": position.created_at.date().isoformat(),
                "employmentType": {"full_time": "FULL_TIME", "part_time": "PART_TIME", "contract": "CONTRACTOR", "internship": "INTERN"}[position.job_type],
                "hiringOrganization": {"@type": "Organization", "name": "Xvera Labs", "sameAs": request.build_absolute_uri("/")},
                "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "Lahore", "addressCountry": "PK"}},
            }
            if position.work_mode == "remote":
                data["jobLocationType"] = "TELECOMMUTE"
                data["applicantLocationRequirements"] = {"@type": "Country", "name": "Pakistan"}
            if position.deadline:
                data["validThrough"] = position.deadline.isoformat()
            ld = json.dumps(data).replace("</", "<\\/")
        return {"jobposting_ld": ld}


# ------------------------------ staff-only CV download ------------------------------
@user_passes_test(
    lambda user: user.is_active and user.is_staff,
    login_url="dashboard:login",
)
def cv_download(request, pk):
    app = get_object_or_404(JobApplication, pk=pk)
    if not app.cv:
        raise Http404
    ext = Path(app.cv.name).suffix
    return FileResponse(app.cv.open("rb"), as_attachment=True, filename=f"{app.reference}-{app.full_name.replace(' ', '_')}{ext}")