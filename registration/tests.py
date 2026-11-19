from django.test import TestCase
from django.urls import reverse

from .models import Student


class RegistrationPageTests(TestCase):
    def test_registration_page_loads(self):
        response = self.client.get('/registration/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration.html')

    def test_registration_success_page_loads(self):
        response = self.client.get('/registration/success/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/success.html')

    def test_registration_creates_student(self):
        response = self.client.post(reverse('student_registration'), {
            'student_id': 'S100',
            'first_name': 'Alex',
            'last_name': 'Rivera',
            'gender': 'Male',
            'date_of_birth': '2005-01-15',
            'contact_number': '5551234',
        })

        self.assertRedirects(response, reverse('registration_success'))
        self.assertTrue(Student.objects.filter(student_id='S100').exists())

    def test_student_list_and_detail(self):
        student = Student.objects.create(
            student_id='S101',
            first_name='Jamie',
            last_name='Lee',
            gender='Female',
            date_of_birth='2005-02-20',
            contact_number='5555678',
        )

        list_response = self.client.get(reverse('student_list'))
        detail_response = self.client.get(reverse('student_detail', args=[student.pk]))

        self.assertContains(list_response, 'S101')
        self.assertContains(detail_response, 'Jamie')

    def test_student_list_searches_by_id_and_name(self):
        matching_student = Student.objects.create(
            student_id='S203',
            first_name='Morgan',
            last_name='Santos',
            gender='Female',
            date_of_birth='2005-04-12',
            contact_number='5551234',
        )
        Student.objects.create(
            student_id='S204',
            first_name='Casey',
            last_name='Reyes',
            gender='Male',
            date_of_birth='2005-06-18',
            contact_number='5555678',
        )

        for search_term in ('S203', 'Morgan', 'santos'):
            with self.subTest(search_term=search_term):
                response = self.client.get(
                    reverse('student_list'),
                    {'q': search_term},
                )

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Morgan')
                self.assertNotContains(response, 'Casey')
                self.assertEqual(
                    list(response.context['students']),
                    [matching_student],
                )

    def test_student_can_be_updated_and_deleted(self):
        student = Student.objects.create(
            student_id='S102',
            first_name='Taylor',
            last_name='Kim',
            gender='Male',
            date_of_birth='2004-10-10',
            contact_number='5550000',
        )
        update_url = reverse('student_update', args=[student.pk])
        response = self.client.post(update_url, {
            'student_id': 'S102',
            'first_name': 'Jordan',
            'last_name': 'Kim',
            'gender': 'Male',
            'date_of_birth': '2004-10-10',
            'contact_number': '5550000',
        })

        self.assertRedirects(response, reverse('student_detail', args=[student.pk]))
        student.refresh_from_db()
        self.assertEqual(student.first_name, 'Jordan')

        delete_response = self.client.post(reverse('student_delete', args=[student.pk]))
        self.assertRedirects(delete_response, reverse('student_list'))
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())
