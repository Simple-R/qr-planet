from django.test import TestCase, Client
from django.urls import reverse

# import requests

client = Client()

class TestUrl(TestCase):
    """Test all Urls"""
    def test_base_url_return404(self):
        response = self.client.get("/qr-gen/api")
        self.assertEqual(response.status_code, 404)
