from django.test import TestCase, Client
from django.urls import reverse

# import requests

class QRGeneratorrURLTest(TestCase):
    def test_home_url(self):
        response = self.client.get("/qr-gen/")
        self.assertEqual(response.status_code, 200)
