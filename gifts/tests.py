from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from users.models import User

from .models import Gift, Review, ReviewVote


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


class GiftEditTest(TestCase):
    def setUp(self):
        self.suggester = User.objects.create_user(
            username="suggester", password="testpass"
        )
        self.other_user = User.objects.create_user(
            username="other", password="testpass2"
        )
        self.gift = Gift.objects.create(
            name="Test Gift",
            description="A nice test gift",
            priceMin=10,
            priceMax=20,
            suggestedBy=self.suggester,
        )
        self.edit_url = reverse("gifts:gift_update", args=[self.gift.id])

    def test_edit_link_visible_for_suggester(self):
        self.client.login(username="suggester", password="testpass")
        response = self.client.get(reverse("users:wishlist"))
        self.assertContains(response, "Edit")

    def test_edit_link_not_visible_for_other_user(self):
        self.client.login(username="other", password="testpass2")
        response = self.client.get(reverse("gifts:search"))
        self.assertNotContains(response, "Edit")

    def test_suggester_can_edit_gift(self):
        self.client.login(username="suggester", password="testpass")
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            self.edit_url,
            {
                "name": "Updated Name",
                "description": "Updated Description",
                "priceMin": 15,
                "priceMax": 25,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.gift.refresh_from_db()
        self.assertEqual(self.gift.name, "Updated Name")

    def test_other_user_cannot_edit_gift(self):
        self.client.login(username="other", password="testpass2")
        response = self.client.get(self.edit_url)
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.status_code in [403, 302])


class ReviewVoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.gift = Gift.objects.create(
            name="Test Gift",
            description="Just a test gift.",
            priceMin=10,
            priceMax=20,
            average_rating=0.0,
        )
        self.review = Review.objects.create(gift=self.gift, author=self.user, rating=5)

    def test_upvote_flow(self):
        self.assertEqual(self.review.score, 0)

        self.client.login(username="testuser", password="testpass")
        vote = ReviewVote.objects.create(review=self.review, user=self.user, vote=1)

        self.review.refresh_from_db()
        self.gift.refresh_from_db()

        self.assertAlmostEqual(self.review.score, 1)
        self.assertAlmostEqual(float(self.gift.average_rating), 5.0)

        vote.vote = -1
        vote.save()
        self.review.refresh_from_db()
        self.gift.refresh_from_db()

        self.assertAlmostEqual(self.review.score, -1)
        self.assertAlmostEqual(float(self.gift.average_rating), 5.0)

    def test_multiple_reviews(self):
        user2 = User.objects.create_user(username="other", password="testpass2")
        review2 = Review.objects.create(gift=self.gift, author=user2, rating=3)

        ReviewVote.objects.create(review=self.review, user=self.user, vote=1)
        ReviewVote.objects.create(review=self.review, user=user2, vote=1)

        self.review.refresh_from_db()
        review2.refresh_from_db()
        self.gift.refresh_from_db()

        # average_rating = 5*3 + 3*1 / (3+1) = 4.5
        self.assertAlmostEqual(float(self.gift.average_rating), 4.5)
