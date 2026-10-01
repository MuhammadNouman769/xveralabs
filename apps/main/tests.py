from django.test import Client, TestCase, override_settings
from django.urls import path

from core.urls import urlpatterns as project_urlpatterns


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
