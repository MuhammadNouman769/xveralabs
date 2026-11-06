from io import StringIO

from django.core.management import call_command
from django.db.models import Count, Q
from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.html import escape

from .catalog import (
    AI_CATEGORIES,
    INDUSTRY_CATEGORIES,
    SERVICE_CATEGORIES,
    SOLUTION_CATEGORIES,
    build_ai_pages,
    build_catalog_pages,
    build_domain_pages,
)
from .models import ServicePage
from .routes import SERVICE_ROUTES


class ServicePageRouteTests(SimpleTestCase):
    def test_strategy_page_urls_remain_available(self):
        self.assertEqual(reverse("strategy_and_consulting"), "/services/strategy-and-consulting/")

    def test_advanced_technology_pages_use_the_shared_view(self):
        page_routes = {
            "advanced_technology": ("advanced-technology", "/services/advanced-technology/"),
            "robotic_process_automation": ("robotic-process-automation", "/services/robotic-process-automation/"),
            "internet_of_things": ("internet-of-things", "/services/internet-of-things/"),
            "blockchain": ("blockchain", "/services/blockchain/"),
            "ar_vr": ("ar-vr", "/services/ar-vr/"),
        }

        for route_name, (slug, path) in page_routes.items():
            with self.subTest(route_name=route_name):
                match = resolve(path)
                self.assertEqual(reverse(route_name), path)
                self.assertEqual(match.url_name, route_name)
                self.assertEqual(match.kwargs["slug"], slug)

    def test_every_service_catalog_route_resolves(self):
        for slug, (route, route_name) in SERVICE_ROUTES.items():
            with self.subTest(slug=slug):
                path = f"/services/{route}"
                self.assertEqual(reverse(route_name), path)
                self.assertEqual(resolve(path).kwargs["slug"], slug)


class ServiceCatalogSeedTests(TestCase):
    def test_seed_command_creates_all_catalog_pages_and_is_idempotent(self):
        call_command("seed_services", stdout=StringIO())
        expected_count = (
            10
            + len(build_catalog_pages())
            + len(build_ai_pages())
            + len(build_domain_pages(SOLUTION_CATEGORIES, "solution"))
            + len(build_domain_pages(INDUSTRY_CATEGORIES, "industry"))
        )
        self.assertEqual(ServicePage.objects.count(), expected_count)

        call_command("seed_services", stdout=StringIO())
        self.assertEqual(ServicePage.objects.count(), expected_count)
        faq_counts = list(
            ServicePage.objects.annotate(
                faq_count=Count(
                    "blocks",
                    filter=Q(blocks__kind="faq", blocks__is_active=True),
                )
            ).values_list("faq_count", flat=True)
        )
        self.assertEqual(len(faq_counts), expected_count)
        self.assertTrue(all(count >= 10 for count in faq_counts))

    def test_seed_command_adds_long_form_content_to_catalog_pages(self):
        call_command("seed_services", stdout=StringIO())
        group_slugs = {
            category["slug"]
            for category in (
                SERVICE_CATEGORIES + AI_CATEGORIES
                + SOLUTION_CATEGORIES + INDUSTRY_CATEGORIES
            )
        }
        section_counts = list(
            ServicePage.objects.filter(group__slug__in=group_slugs)
            .annotate(
                section_count=Count(
                    "blocks",
                    filter=Q(blocks__kind="section", blocks__is_active=True),
                )
            )
            .values_list("section_count", flat=True)
        )

        self.assertTrue(section_counts)
        self.assertTrue(all(count >= 3 for count in section_counts))

    def test_every_service_page_and_navigation_renders(self):
        call_command("seed_services", stdout=StringIO())

        for slug, (route, _) in SERVICE_ROUTES.items():
            with self.subTest(slug=slug):
                response = self.client.get(f"/services/{route}")
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, f'href="/services/{route}"')

    def test_ai_menu_pages_render_without_remote_images(self):
        call_command("seed_services", stdout=StringIO())

        for page in build_ai_pages():
            with self.subTest(slug=page["slug"]):
                response = self.client.get(f"/services/{page['slug']}/")
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, "images.unsplash.com")
                self.assertContains(response, "sv-ai-layout-")
                self.assertContains(response, "sv-ai-visual__core")
                self.assertContains(response, "sv-ai-visual__orbit")

    def test_solution_and_industry_pages_render_with_card_styles(self):
        call_command("seed_services", stdout=StringIO())
        pages = (
            build_domain_pages(SOLUTION_CATEGORIES, "solution")
            + build_domain_pages(INDUSTRY_CATEGORIES, "industry")
        )

        for page in pages:
            with self.subTest(slug=page["slug"]):
                response = self.client.get(f"/services/{page['slug']}/")
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, escape(page["title"]))
                self.assertContains(response, "sv-card-style-")