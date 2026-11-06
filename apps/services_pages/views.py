import json

from django.shortcuts import get_object_or_404, render
from django.views import View

from .catalog import (
    AI_CATEGORIES,
    INDUSTRY_CATEGORIES,
    SERVICE_CATEGORIES,
    SOLUTION_CATEGORIES,
)
from .models import BlockKind, ServicePage
from .routes import SERVICE_ROUTES

CATALOG_GROUPS = {
    category["slug"]
    for category in (*SERVICE_CATEGORIES, *SOLUTION_CATEGORIES, *INDUSTRY_CATEGORIES)
}


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
        if page.group.slug in CATALOG_GROUPS:
            template_name = "services/catalog_service_page.html"
            design_variant = list(SERVICE_ROUTES).index(page.slug)
            ctx["design_variant"] = design_variant
            ctx["card_style"] = design_variant % 8
        elif page.group.slug == "advanced-technology":
            template_name = "services/technology_page.html"
        elif page.group.slug in {category["slug"] for category in AI_CATEGORIES}:
            template_name = "services/ai_service_page.html"
            category_index = next(
                index
                for index, category in enumerate(AI_CATEGORIES)
                if category["slug"] == page.group.slug
            )
            category = AI_CATEGORIES[category_index]
            page_position = next(
                index
                for index, title in enumerate(category["items"])
                if title == page.title
            )
            ctx["ai_layout"] = category_index * len(category["items"]) + page_position
            ctx["ai_layout_variant"] = (category_index + page_position * 2) % 8
            ctx["ai_page_number"] = f"{ctx['ai_layout'] + 1:02d}"
            ctx["ai_title_pattern"] = (
                "Machine learning with human direction",
                "A focused path from problem to solution",
                "Built to fit your existing workflows",
                "Clear, careful, and ready to evolve",
            )[page_position]
        else:
            template_name = self.template_name
        return render(request, template_name, ctx)
