from django.test import TestCase


class LandingPageTests(TestCase):
    def test_site_root_displays_landing_page(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/landing.html')
