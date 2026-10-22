from django.test import TestCase


class RegistrationPageTests(TestCase):
    def test_registration_page_loads(self):
        response = self.client.get('/registration/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')

    def test_registration_success_page_loads(self):
        response = self.client.get('/registration/success/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/success.html')
