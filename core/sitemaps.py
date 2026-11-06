from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blogs.models import Resource
from apps.main.models import IndustryCaseStudy
from apps.services_pages.models import ServicePage
from apps.services_pages.routes import SERVICE_ROUTES


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = "https"

    page_names = [
        "home",
        "about-us",
        "why_choose_us",
        "contact_us",
        "case_studies",
        "resources",
        "faqs",
        "term_condition",
        "privacy_policy",
        "site_map",
        "careeers",
        "career_apply",
        "life_at_xvera_labs",
        "people",
        "campus_ambassador_program",
        "partners",
        "partners_investors",
        "partner_apply",
    ]

    def items(self):
        return self.page_names

    def location(self, item):
        return reverse(item)


class ServicePageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = "https"

    def items(self):
        published_slugs = set(
            ServicePage.objects.filter(
                is_active=True,
                is_published=True,
                slug__in=SERVICE_ROUTES,
            ).values_list("slug", flat=True)
        )
        return [
            route_name
            for slug, (_, route_name) in SERVICE_ROUTES.items()
            if slug in published_slugs
        ]

    def location(self, item):
        return reverse(item)


class ResourceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    protocol = "https"

    def items(self):
        return Resource.objects.filter(is_published=True)

    def location(self, item):
        return reverse("resource_detail", args=[item.slug])


class IndustryCaseStudySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    protocol = "https"

    def items(self):
        return IndustryCaseStudy.objects.filter(is_active=True, is_published=True)

    def location(self, item):
        return reverse("case_study_detail", args=[item.slug])


PUBLIC_SITEMAPS = {
    "static": StaticViewSitemap,
    "services": ServicePageSitemap,
    "resources": ResourceSitemap,
    "industry-case-studies": IndustryCaseStudySitemap,
}
