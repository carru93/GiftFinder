from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from users.models import User

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


class MarkAsOwnedTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = Client()
        self.client.login(username="testuser", password="testpass")

        self.gift = Gift.objects.create(
            name="Test Gift", description="A nice test gift", priceMin=10, priceMax=20
        )
        self.url = reverse("gifts:mark_as_owned", args=[self.gift.id])

    def test_mark_as_owned(self):
        self.assertFalse(self.user.possessed_gifts.filter(id=self.gift.id).exists())

        response = self.client.post(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.possessed_gifts.filter(id=self.gift.id).exists())

    def test_mark_as_owned_twice(self):
        self.client.post(self.url, follow=True)
        self.user.refresh_from_db()
        self.assertTrue(self.user.possessed_gifts.filter(id=self.gift.id).exists())

        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.user.possessed_gifts.filter(id=self.gift.id).count(), 1)
