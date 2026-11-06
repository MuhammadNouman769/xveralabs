from io import StringIO

from django.core.management import call_command
from django.test import Client, TestCase, override_settings
from django.urls import path, reverse
from django.utils.html import escape

from core.urls import urlpatterns as project_urlpatterns
from .case_studies import INDUSTRY_CASE_STUDIES
from .models import IndustryCaseStudy, IndustryCaseStudyBlock
from apps.services_pages.models import ServiceGroup, ServicePage


def raise_server_error(request):
	raise RuntimeError('Intentional error-page test.')


urlpatterns = [
	path('__test-server-error__/', raise_server_error),
	*project_urlpatterns,
]


class ErrorPageTests(TestCase):
	@override_settings(
		DEBUG=False,
		ROOT_URLCONF=__name__,
		ALLOWED_HOSTS=['testserver'],
		SECURE_SSL_REDIRECT=False,
	)
	def test_custom_not_found_page_is_rendered(self):
		response = self.client.get('/__test-not-found__/')

		self.assertEqual(response.status_code, 404)
		self.assertTemplateUsed(response, '404.html')
		self.assertContains(response, "We couldn't find that page", status_code=404)

	@override_settings(
		DEBUG=False,
		ROOT_URLCONF=__name__,
		ALLOWED_HOSTS=['testserver'],
		SECURE_SSL_REDIRECT=False,
	)
	def test_custom_server_error_page_is_rendered(self):
		response = Client(raise_request_exception=False).get('/__test-server-error__/')

		self.assertEqual(response.status_code, 500)
		self.assertTemplateUsed(response, '500.html')
		self.assertContains(response, 'Something went wrong.', status_code=500)

	@override_settings(
		DEBUG=True,
		ALLOWED_HOSTS=['testserver'],
		SECURE_SSL_REDIRECT=False,
	)
	def test_homepage_loads_scoped_static_assets_without_inline_styles(self):
		response = self.client.get('/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'page-home-index')
		self.assertContains(response, '/static/css/pages/home-index.css')
		self.assertNotContains(response, '<style')
		self.assertNotContains(response, ' style=')

	def test_legacy_pages_redirect_to_live_destinations(self):
		destinations = {
			'/signin/': '/',
			'/signup/': '/',
			'/services/': '/services/software-development/',
			'/projects/': '/case-studies/',
			'/blog-single/': '/resources/',
			'/art/': '/services/ai-solutions-engineering/',
			'/sqa/': '/services/quality-assurance/',
			'/web-development/': '/services/web-app-development/',
			'/product-development/': '/services/product-engineering/',
			'/dev-ops/': '/services/cloud-native-engineering/',
			'/staff-augmentation/': '/services/staff-augmentation/',
			'/blogs/': '/resources/',
		}

		for path, destination in destinations.items():
			with self.subTest(path=path):
				response = self.client.get(path)

				self.assertEqual(response.status_code, 301)
				self.assertEqual(response['Location'], destination)


class SitemapTests(TestCase):
	def setUp(self):
		call_command('seed_case_studies', stdout=StringIO())
		group = ServiceGroup.objects.create(
			name='Software Development',
			slug='software-development',
		)
		ServicePage.objects.create(
			group=group,
			title='Web App Development',
			slug='web-app-development',
			tagline='Build a web product.',
			intro='A published service page.',
			is_published=True,
		)

	def test_robots_points_to_both_sitemaps_on_the_current_domain(self):
		response = self.client.get('/robots.txt', HTTP_HOST='testserver')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Sitemap: https://testserver/sitemap.xml')
		self.assertContains(response, 'Sitemap: https://testserver/sitemap.txt')

	def test_xml_and_text_sitemaps_include_service_resource_and_industry_pages(self):
		xml_response = self.client.get('/sitemap.xml', HTTP_HOST='testserver')
		text_response = self.client.get('/sitemap.txt', HTTP_HOST='testserver')

		self.assertEqual(xml_response.status_code, 200)
		self.assertEqual(text_response.status_code, 200)
		self.assertContains(xml_response, 'https://testserver/')
		self.assertContains(text_response, 'https://testserver/')
		for path in (
			'/services/web-app-development/',
			'/resources/cloud-cost-controls-without-slowing-delivery/',
			'/case-studies/healthcare/',
			'/case-studies/fintech/',
			'/case-studies/e-commerce/',
			'/case-studies/education/',
			'/case-studies/logistics/',
		):
			with self.subTest(path=path):
				self.assertContains(xml_response, path)
				self.assertContains(text_response, path)

	def test_html_sitemap_lists_public_pages_and_is_linked_from_footer(self):
		response = self.client.get(reverse('site_map'))
		home_response = self.client.get(reverse('home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Website sitemap')
		self.assertContains(response, 'Web App Development')
		self.assertContains(response, '/services/web-app-development/')
		self.assertContains(response, 'Industry case studies')
		self.assertContains(response, reverse('sitemap'))
		self.assertContains(home_response, reverse('site_map'))

	def test_terms_page_uses_shared_legal_layout_and_section_navigation(self):
		response = self.client.get(reverse('term_condition'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Terms of Use')
		self.assertContains(response, 'faqs-privacy_policy.css')
		self.assertContains(response, 'href="#acceptance"')
		self.assertContains(response, 'id="contact"')


class IndustryCaseStudyTests(TestCase):
	def setUp(self):
		call_command('seed_case_studies', stdout=StringIO())

	def test_case_study_index_uses_published_backend_records(self):
		response = self.client.get(reverse('case_studies'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['case_studies'].count(), 5)
		self.assertContains(response, 'page-case-studies')
		for study in IndustryCaseStudy.objects.filter(is_published=True):
			self.assertContains(
				response,
				reverse('case_study_detail', args=[study.slug]),
			)

	def test_each_industry_has_a_dynamic_detail_page_and_image(self):
		for entry in INDUSTRY_CASE_STUDIES:
			with self.subTest(slug=entry['slug']):
				response = self.client.get(
					reverse('case_study_detail', args=[entry['slug']])
				)

				self.assertEqual(response.status_code, 200)
				self.assertContains(response, entry['title'])
				self.assertContains(response, escape(entry['image']))
				self.assertContains(response, 'Capabilities to consider')
				self.assertContains(response, 'property="og:title"')
				self.assertContains(response, '"@type":"WebPage"')

	def test_case_study_seed_is_idempotent_and_creates_content_blocks(self):
		call_command('seed_case_studies', stdout=StringIO())
		self.assertEqual(IndustryCaseStudy.objects.count(), 5)
		self.assertEqual(IndustryCaseStudyBlock.objects.count(), 35)

	def test_unpublished_case_study_is_not_public(self):
		study = IndustryCaseStudy.objects.get(slug='healthcare')
		study.is_published = False
		study.save(update_fields=['is_published'])

		self.assertEqual(
			self.client.get(
				reverse('case_study_detail', args=[study.slug])
			).status_code,
			404,
		)

	def test_detail_page_reflects_dashboard_edits_from_the_database(self):
		study = IndustryCaseStudy.objects.get(slug='healthcare')
		study.title = 'Updated healthcare case study title'
		study.save(update_fields=['title'])

		response = self.client.get(
			reverse('case_study_detail', args=[study.slug])
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Updated healthcare case study title')
