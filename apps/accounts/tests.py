from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UserTests(TestCase):
    def test_create_user_positive(self):
        user = User.objects.create_user(
            email='test@example.com', password='testpass123')
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        self.assertTrue(user.check_password('testpass123'))

    def test_create_user_duplicate_email_negative(self):
        User.objects.create_user(
            email='test@example.com', password='testpass123')
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@example.com', password='testpass456')

    def test_login_positive(self):
        User.objects.create_user(
            email='test@example.com', password='testpass123')
        login = self.client.login(
            email='test@example.com', password='testpass123')
        self.assertTrue(login)

    def test_login_wrong_password_negative(self):
        User.objects.create_user(
            email='test@example.com', password='testpass123')
        login = self.client.login(
            email='test@example.com', password='wrongpass')
        self.assertFalse(login)

    def test_profile_update_positive(self):
        user = User.objects.create_user(
            email='test@example.com', password='testpass123', first_name='Old')
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post(reverse('accounts:profile'), {
                                    'first_name': 'New', 'last_name': 'User', 'email': 'test@example.com'})
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'New')

    def test_profile_update_unauthenticated_negative(self):
        response = self.client.post(
            reverse('accounts:profile'), {'first_name': 'New'})
        self.assertNotEqual(response.status_code, 200)
