from django.test import TestCase
from django.urls import reverse


class LifeAtXveraAssetTests(TestCase):
	def test_culture_page_provides_image_base_and_external_assets(self):
		response = self.client.get(reverse('life_at_xvera_labs'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'data-culture-image-base="/static/images/culture/"')
		self.assertContains(response, '/static/css/pages/about-culture.css')
		self.assertContains(response, '/static/js/pages/about-culture-1.js')
		self.assertNotContains(response, "{% static 'images/culture/")
