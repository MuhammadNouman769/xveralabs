from urllib import request
from django.shortcuts import render
import json

from django.shortcuts import get_object_or_404, render
from django.views import View

from .models import BlockKind, ServicePage


class ServicePageView(View):
    template_name = "services/service_page.html"      # adjust to where you put the template

    def get(self, request, **kwargs):
        page = get_object_or_404(ServicePage.objects.select_related("group"), slug=kwargs["slug"], is_published=True)
        by_kind = {}
        for b in page.blocks.filter(is_active=True): # type: ignore
            by_kind.setdefault(b.kind, []).append(b)
        siblings = list(ServicePage.objects.filter(group=page.group, is_published=True))
        faqs = by_kind.get(BlockKind.FAQ, [])
        faq_ld = None
        if faqs:
            faq_ld = json.dumps({
                "@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": f.title,
                                "acceptedAnswer": {"@type": "Answer", "text": f.text}} for f in faqs],
            }).replace("</", "<\\/")
        ctx = {
            "page": page, "group": page.group, "siblings": siblings,
            "others": [p for p in siblings if p.pk != page.pk],
            "features": by_kind.get(BlockKind.FEATURE, []), "steps": by_kind.get(BlockKind.STEP, []),
            "deliverables": by_kind.get(BlockKind.DELIVERABLE, []), "audience": by_kind.get(BlockKind.AUDIENCE, []),
            "sections": by_kind.get(BlockKind.SECTION, []), "faqs": faqs, "faq_ld": faq_ld,
        }
        return render(request, self.template_name, ctx)










def advanced_technology(request):
    return render(request, 'services/advanced_technology/advanced_technology.html')

def robotic_process_automation(request):
    return render(request, 'services/advanced_technology/robotic_process_automation.html')

def internet_of_things(request):
    return render(request, 'services/advanced_technology/internet_of_things.html')

def blockchain(request):
    return render(request, 'services/advanced_technology/blockchain.html')

def ar_vr(request):
    return render(request, 'services/advanced_technology/ar_vr.html')
