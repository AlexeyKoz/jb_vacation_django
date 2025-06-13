from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.models import Country
from .models import Vacation, Like

User = get_user_model()


class VacationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com', password='testpass123')
        self.country = Country.objects.create(name='Testland')

    def test_create_vacation_positive(self):
        self.client.login(email='user@example.com', password='testpass123')
        vacation = Vacation.objects.create(
            country=self.country,
            description='A test vacation',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=1000
        )
        self.assertTrue(Vacation.objects.filter(
            description='A test vacation').exists())

    def test_create_vacation_invalid_dates_negative(self):
        with self.assertRaises(Exception):
            Vacation.objects.create(
                country=self.country,
                description='Invalid dates',
                start_date='2030-01-10',
                end_date='2030-01-01',
                price=1000
            )

    def test_create_vacation_negative_price_negative(self):
        with self.assertRaises(Exception):
            Vacation.objects.create(
                country=self.country,
                description='Negative price',
                start_date='2030-01-01',
                end_date='2030-01-10',
                price=-100
            )

    def test_list_vacations_positive(self):
        Vacation.objects.create(
            country=self.country,
            description='List test',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=1000
        )
        response = self.client.get(reverse('vacations:vacation_list'))
        self.assertContains(response, 'List test')

    def test_like_vacation_positive(self):
        vacation = Vacation.objects.create(
            country=self.country,
            description='Like test',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=1000
        )
        self.client.login(email='user@example.com', password='testpass123')
        response = self.client.post(
            reverse('vacations:vacation_like', args=[vacation.id]))
        self.assertEqual(Like.objects.filter(
            user=self.user, vacation=vacation).count(), 1)

    def test_like_vacation_unauthenticated_negative(self):
        vacation = Vacation.objects.create(
            country=self.country,
            description='Like unauth',
            start_date='2030-01-01',
            end_date='2030-01-10',
            price=1000
        )
        response = self.client.post(
            reverse('vacations:vacation_like', args=[vacation.id]))
        self.assertNotEqual(response.status_code, 200)
