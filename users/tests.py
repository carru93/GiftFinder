from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from gifts.models import Gift
from hobbies.models import Hobby

from .models import User


class UsersTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="testpass2"
        )

        self.hobby = Hobby.objects.create(name="Reading")
        self.gift = Gift.objects.create(
            name="Test Gift",
            description="A test gift",
            priceMin=10,
            priceMax=20,
        )

    # SIGNUP #
    def test_registration_page_view(self):
        url = reverse("users:signup")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username")
        self.assertContains(response, "email")

    def test_registration_valid_form(self):
        url = reverse("users:signup")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "Supersecret123",
            "password2": "Supersecret123",
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            User.objects.get(username="newuser").id,
        )

    def test_registration_invalid_form(self):
        url = reverse("users:signup")
        data = {
            "username": "inv",
            "email": "invalid",
            "password1": "short",
            "password2": "abc",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="inv").exists())

    # LOGIN/LOGOUT #
    def test_login_valid(self):
        url = reverse("users:login")
        data = {"username": "testuser", "password": "testpass"}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.id)

    def test_login_invalid(self):
        url = reverse("users:login")
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_logout(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("users:logout")
        self.client.get(url, follow=True)
        self.assertNotIn("_auth_user_id", self.client.session)

    # PROTECTED #
    def test_profile_view_not_logged_in(self):
        url = reverse("users:profile")
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f"{reverse('users:login')}?next={url}")

    def test_profile_view_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "content profile")

    # USER SETTINGS (UserUpdateView) #
    def test_update_profile_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("users:settings")
        data = {
            "username": "testuser",
            "email": "newemail@example.com",
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(
                "Your profile has been updated successfully!" in str(m)
                for m in messages
            )
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")

    def test_update_profile_not_logged_in(self):
        url = reverse("users:settings")
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f"{reverse('users:login')}?next={url}")

    # WISHLIST #
    def test_wishlist_view(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("users:wishlist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No gift wished yet.")
        self.assertNotContains(response, "Test Gift")

        self.gift.suggestedBy = self.user
        self.gift.save()
        response = self.client.get(url)
        self.assertContains(response, "Test Gift")

    # FRIENDS #
    def test_friends_list_view(self):
        url = reverse("users:friends")
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f"{reverse('users:login')}?next={url}")

        self.client.login(username="testuser", password="testpass")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No friends yet")

        self.user.friends.add(self.other_user)
        response = self.client.get(url)
        self.assertContains(response, "otheruser")

    def test_search_friends_view(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("users:search_friends")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "otheruser")

        response = self.client.get(url, {"filter": "other"})
        self.assertContains(response, "otheruser")

        response = self.client.get(url, {"filter": "abc"})
        self.assertNotContains(response, "otheruser")

    def test_toggle_follow_user(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("users:toggle_follow_user", args=[self.other_user.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.friends.filter(id=self.other_user.id).exists())

        response = self.client.post(url, follow=True)
        self.assertFalse(self.user.friends.filter(id=self.other_user.id).exists())

    # SUGGESTED GIFTS #
    def test_suggested_gifts_view(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("users:suggested_gifts")
        response = self.client.get(url)
        self.assertContains(response, "complete your profile")

        self.user.birth_date = "2004-01-01"
        self.user.gender = "M"
        self.user.location = "New York"
        self.user.save()
        self.user.hobbies.add(self.hobby)

        self.gift.suggestedBy = self.other_user
        self.gift.hobbies.add(self.hobby)
        self.gift.suitable_age_range = "18-24"
        self.gift.suitable_gender = "M"
        self.gift.suitable_location = "new york"
        self.gift.save()

        response = self.client.get(url)

        self.assertNotContains(response, "complete your profile")
        self.assertContains(response, "Test Gift")

        self.user.possessed_gifts.add(self.gift)
        response = self.client.get(url)
        self.assertNotContains(response, "Test Gift")

    # UI PROFILE #
    def test_navbar_highlight(self):
        self.client.login(username="testuser", password="testpass")
        wishlist_url = reverse("users:wishlist")
        response = self.client.get(wishlist_url)
        self.assertContains(response, 'bg-primary font-semibold">')

        friends_url = reverse("users:friends")
        response = self.client.get(friends_url)
        self.assertContains(response, 'bg-primary font-semibold">')
        self.assertNotContains(
            response,
            'Wishlist</a></li><li class="px-4 py-2 mt-2 bg-primary font-semibold"',
        )

    def test_messages_frontend(self):
        self.client.login(username="testuser", password="testpass")
        settings_url = reverse("users:settings")
        data = {"username": "testuser", "email": "updated@example.com"}
        response = self.client.post(settings_url, data, follow=True)
        self.assertContains(response, "Your profile has been updated successfully!")
