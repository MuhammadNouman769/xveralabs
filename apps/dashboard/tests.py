import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.blogs.models import Resource
from apps.contact.models import ContactMessage
from apps.expenses.models import Expense
from apps.services_pages.models import ServiceGroup, ServicePage


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="dashboard-admin",
            email="admin@example.com",
            password="Secure-unrelated-password-992!",
        )

    def test_dashboard_requires_staff_login(self):
        response = self.client.get(reverse("dashboard:home"))

        self.assertRedirects(
            response,
            f"{reverse('dashboard:login')}?next={reverse('dashboard:home')}",
        )

    def test_non_staff_user_cannot_sign_in_to_dashboard(self):
        get_user_model().objects.create_user(
            username="visitor",
            password="Secure-unrelated-password-992!",
        )

        response = self.client.post(
            reverse("dashboard:login"),
            {
                "username": "visitor",
                "password": "Secure-unrelated-password-992!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "does not have dashboard access")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_django_admin_route_is_removed_without_deleting_data(self):
        group = ServiceGroup.objects.create(name="Existing group", slug="existing-group")

        response = self.client.get("/admin/")

        self.assertEqual(response.status_code, 404)
        self.assertTrue(ServiceGroup.objects.filter(pk=group.pk).exists())

    def test_superuser_can_open_dashboard_and_all_modules(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("dashboard:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage the moving parts")
        self.assertContains(response, "Resources")
        self.assertContains(response, "Staff accounts")

    def test_staff_access_respects_model_permissions(self):
        staff = get_user_model().objects.create_user(
            username="content-editor",
            password="Secure-unrelated-password-992!",
            is_staff=True,
        )
        permission = Permission.objects.get(
            content_type__app_label="services_pages",
            codename="view_servicepage",
        )
        staff.user_permissions.add(permission)
        self.client.force_login(staff)

        listing = self.client.get(reverse("dashboard:section", args=["services"]))
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(
            self.client.post(
                reverse("dashboard:create", args=["services"]),
                {},
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(reverse("dashboard:section", args=["users"])).status_code,
            403,
        )

    def test_view_only_staff_can_view_but_not_change_records(self):
        group = ServiceGroup.objects.create(name="Strategy", slug="strategy")
        page = ServicePage.objects.create(
            group=group,
            title="Product planning",
            slug="product-planning",
            tagline="Plan a better product.",
            intro="Description",
        )
        staff = get_user_model().objects.create_user(
            username="read-only",
            password="Secure-unrelated-password-992!",
            is_staff=True,
        )
        staff.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="services_pages",
                codename="view_servicepage",
            )
        )
        self.client.force_login(staff)

        response = self.client.get(
            reverse("dashboard:edit", args=["services", page.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Save changes")
        self.assertEqual(
            self.client.post(
                reverse("dashboard:edit", args=["services", page.pk]),
                {"title": "Changed"},
            ).status_code,
            403,
        )


class DashboardContentTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="dashboard-admin",
            email="admin@example.com",
            password="Secure-unrelated-password-992!",
        )
        self.client.force_login(self.admin)

    def test_resources_are_editable_and_public_content_updates(self):
        resource = Resource.objects.get(slug="cloud-cost-controls-without-slowing-delivery")
        payload = {
            "title": "Cloud economics for product teams",
            "slug": resource.slug,
            "category": resource.category,
            "topic": resource.topic,
            "kind": resource.kind,
            "read_time": resource.read_time,
            "excerpt": "Updated by the dashboard.",
            "image": resource.image,
            "image_alt": resource.image_alt,
            "sections": json.dumps(resource.sections),
            "order": resource.order,
            "is_published": "on",
        }

        response = self.client.post(
            reverse("dashboard:edit", args=["resources", resource.pk]),
            payload,
        )

        self.assertRedirects(
            response,
            reverse("dashboard:edit", args=["resources", resource.pk]),
        )
        resource.refresh_from_db()
        self.assertEqual(resource.title, "Cloud economics for product teams")
        self.assertContains(self.client.get("/resources/"), resource.title)

    def test_resource_creation_rejects_invalid_structured_content(self):
        response = self.client.post(
            reverse("dashboard:create", args=["resources"]),
            {
                "title": "Invalid article",
                "slug": "invalid-article",
                "category": "Technology",
                "topic": "technology",
                "kind": "article",
                "read_time": "1 min",
                "excerpt": "Excerpt",
                "image": "https://example.com/image.jpg",
                "image_alt": "Example image",
                "sections": "{bad json}",
                "order": "0",
                "is_published": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors["sections"])
        self.assertFalse(Resource.objects.filter(slug="invalid-article").exists())

    def test_contact_submissions_show_private_details_and_allow_status_changes(self):
        contact = ContactMessage.objects.create(
            topic="new_project",
            full_name="Alex Example",
            email="alex@example.com",
            phone="5550100",
            company="Example Inc",
            region="north_america",
            services=["web"],
            details="Private project details",
        )

        response = self.client.get(
            reverse("dashboard:edit", args=["contacts", contact.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Private project details")
        self.assertContains(response, "Read-only visitor information")
        self.assertNotContains(response, 'name="full_name"')

        response = self.client.post(
            reverse("dashboard:edit", args=["contacts", contact.pk]),
            {"status": "contacted"},
        )
        self.assertEqual(response.status_code, 302)
        contact.refresh_from_db()
        self.assertEqual(contact.status, "contacted")

    def test_staff_accounts_can_be_created_with_hashed_passwords(self):
        response = self.client.post(
            reverse("dashboard:create", args=["users"]),
            {
                "username": "new-editor",
                "email": "editor@example.com",
                "first_name": "New",
                "last_name": "Editor",
                "password": "Another-unrelated-password-418!",
                "is_active": "on",
                "is_staff": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(username="new-editor")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password("Another-unrelated-password-418!"))

    def test_deletion_requires_post(self):
        group = ServiceGroup.objects.create(name="Temporary", slug="temporary")

        response = self.client.get(
            reverse("dashboard:delete", args=["service-groups", group.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ServiceGroup.objects.filter(pk=group.pk).exists())

        response = self.client.post(
            reverse("dashboard:delete", args=["service-groups", group.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ServiceGroup.objects.filter(pk=group.pk).exists())

    def test_expenses_have_a_separate_module_and_record_who_entered_them(self):
        response = self.client.post(
            reverse("dashboard:create", args=["expenses"]),
            {
                "title": "Cloud hosting",
                "category": "software",
                "expense_date": timezone.localdate().isoformat(),
                "vendor": "Hosting Co",
                "amount": "1250.50",
                "currency": "USD",
                "payment_method": "card",
                "status": "pending",
                "reference": "INV-2048",
                "notes": "Monthly production hosting",
            },
        )

        expense = Expense.objects.get(reference="INV-2048")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(expense.recorded_by, self.admin)

        response = self.client.get(reverse("dashboard:section", args=["expenses"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Company expenses")
        self.assertContains(response, "USD 1,250.50")
        self.assertContains(response, "Pending payments")
        self.assertEqual(response.context["expense_summary"]["pending_count"], 1)

    def test_expense_receipts_are_served_only_to_authorized_staff(self):
        expense = Expense.objects.create(
            title="Office supplies",
            category=Expense.Category.OFFICE,
            expense_date=timezone.localdate(),
            amount="250.00",
            currency=Expense.Currency.PKR,
            payment_method=Expense.PaymentMethod.CASH,
            status=Expense.Status.PAID,
        )

        response = self.client.get(
            reverse("dashboard:expense_receipt", args=[expense.pk])
        )

        self.assertEqual(response.status_code, 404)
