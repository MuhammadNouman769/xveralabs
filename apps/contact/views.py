from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .forms import ContactForm


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    return (forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")) or None


def _notify(msg):
    """Email the team. A mail failure must never lose the saved message."""
    receiver = getattr(settings, "CONTACT_RECEIVER_EMAIL", None)
    if not receiver:
        return
    body = (
        f"Topic: {msg.get_topic_display()}\n"
        f"Name: {msg.full_name}\nEmail: {msg.email}\nPhone: {msg.full_phone}\n"
        f"Company: {msg.company} {msg.company_url}\nRegion: {msg.get_region_display()}\n"
        f"Services: {', '.join(msg.service_labels)}\n\n"
        f"{msg.details}\n"
    )
    send_mail(
        subject=f"[Xvera Labs] New inquiry: {msg.full_name} ({msg.get_topic_display()})",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[receiver],
        fail_silently=True,
    )


class ContactUsView(View):
    template_name = "home/contact-us.html"  # change to your real template path if it differs

    def get(self, request):
        return self._render(request, ContactForm())

    def post(self, request):
        sent_url = f"{reverse('contact_us')}?sent=1#support"
        if request.POST.get("website"):  # honeypot: bots fill it, people never see it
            return redirect(sent_url)
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ip_address = _client_ip(request)
            msg.save()
            _notify(msg)
            return redirect(sent_url)
        return self._render(request, form, status=400)

    def _render(self, request, form, status=200):
        ctx = {"form": form, "sent": request.GET.get("sent") == "1"}
        return render(request, self.template_name, ctx, status=status)