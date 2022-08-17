from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import resolve, reverse, reverse_lazy

User=get_user_model()

client = Client()


class TestUrlUnAuthenticated(TestCase):
    """Test Urls for Unauthenticated Users"""
    
    def test_register(self):
        """Test the url for Register"""
        response = self.client.get('/qr-gen/accounts/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_login_for_anonymous_users(self):
        """This should pass"""
        response = self.client.get('/qr-gen/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')


class TestUrlAuthenticated(TestCase):
    """Test URLS for Authenticated Users"""

    def setUp(self):
        self.user = User.objects.create_user(username="testUser", email='test@testmail.com', password='test_password', is_staff=True)
        self.client = Client()

    def test_register_url(self):
        self.client.login(username='testUser', password='test_password')
        url = reverse('accounts:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_register(self):
        """Test the url for Register"""
        response = self.client.get('/qr-gen/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_redirects_to_home_for_logged_in_users(self):
        """This should fail"""
        self.user, self.client = self.login()
        response = self.client.get('/qr-gen/accounts/register/')
        self.assertEqual(response.status_code, 301)


