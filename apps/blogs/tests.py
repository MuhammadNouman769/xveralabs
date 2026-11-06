from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from .catalog import RESOURCES


class ResourcePageTests(TestCase):
    def test_resource_hub_displays_cards_and_filters(self):
        response = self.client.get(reverse("resources"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Insights on technology, AI and better products")
        self.assertContains(response, 'class="rs-card"')
        self.assertContains(response, "Browse by topic")
        for resource in RESOURCES:
            with self.subTest(slug=resource["slug"]):
                self.assertContains(response, reverse("resource_detail", args=[resource["slug"]]))

    def test_resource_filters_return_the_requested_collection(self):
        response = self.client.get(reverse("resources"), {"filter": "guides"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "An Enterprise AI Readiness Checklist")
        self.assertNotContains(response, "Cloud Cost Controls Without Slowing Delivery")

    def test_resource_detail_shows_rich_content_and_industry_image(self):
        resource = RESOURCES[0]
        response = self.client.get(
            reverse("resource_detail", args=[resource["slug"]])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, resource["title"])
        self.assertContains(response, escape(resource["image"]))
        self.assertContains(response, resource["sections"][0]["heading"])
        self.assertContains(response, resource["sections"][0]["bullets"][0])

    def test_unknown_resource_returns_not_found(self):
        response = self.client.get(reverse("resource_detail", args=["unknown-resource"]))

        self.assertEqual(response.status_code, 404)
