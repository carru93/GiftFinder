from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from .models import Gift


def create_gift(name, priceMin=10, priceMax=100):
    return Gift.objects.create(name=name, priceMin=priceMin, priceMax=priceMax)


class SearchGiftViewTests(TestCase):

    def test_no_gifts(self):
        client = Client()
        response = client.get(reverse("gifts:search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No gifts found matching your criteria.")

    def test_one_gift(self):
        create_gift("test")
        client = Client()
        response = client.get(reverse("gifts:search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="card">', 1)

    def test_multiple_gift(self):
        N = 5
        for i in range(N):
            create_gift(f"gift_${i}")
        client = Client()
        response = client.get(reverse("gifts:search"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="card">', N)

    def test_multiple_gift_filtered_price_min_gte(self):
        N = 5
        for i in range(N):
            create_gift(f"gift_${i}")
        create_gift("valid_gift", 50, 500)
        client = Client()
        response = client.get(reverse("gifts:search") + "?price_min=50")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="card">', 1)
