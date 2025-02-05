from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from forum.models import Comment, Post
from users.models import User


class ForumTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass2"
        )

        self.post1 = Post.objects.create(
            title="First Post", content="Content of the first post", author=self.user
        )
        self.post2 = Post.objects.create(
            title="Second Post",
            content="Another interesting post",
            author=self.other_user,
        )

        self.client = Client()

    # TEST LISTING (PostListView) #
    def test_list_posts_view_status_code(self):
        url = reverse("forum:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum/list.html")

    def test_list_posts_content(self):
        url = reverse("forum:list")
        response = self.client.get(url)
        self.assertContains(response, "First Post")
        self.assertContains(response, "Second Post")

    def test_list_posts_order(self):
        url = reverse("forum:list")
        response = self.client.get(url)
        content = response.content.decode("utf-8")
        self.assertTrue(content.index("Second Post") < content.index("First Post"))

    def test_list_posts_search(self):
        url = reverse("forum:list")
        response = self.client.get(url, {"q": "Another"})
        self.assertContains(response, "Second Post")
        self.assertNotContains(response, "First Post")

    # TEST CREATION (PostCreateView) #
    def test_post_create_view_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("forum:create")
        data = {"title": "New Post", "content": "New Post Content"}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(title="New Post").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("The post has been created!" in str(m) for m in messages))

    def test_post_create_view_not_logged_in(self):
        url = reverse("forum:create")
        data = {"title": "Anon Post", "content": "Content"}
        response = self.client.post(url, data, follow=True)
        self.assertNotEqual(response.redirect_chain, [])
        self.assertFalse(Post.objects.filter(title="Anon Post").exists())

    def test_post_create_view_invalid(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("forum:create")
        data = {"content": "Missing title here"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(content="Missing title here").exists())

    # TEST DETAIL (PostDetailView) #
    def test_post_detail_view(self):
        url = reverse("forum:post_detail", args=[self.post1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forum/post_detail.html")
        self.assertContains(response, "First Post")
        self.assertContains(response, "Content of the first post")

    def test_post_detail_comments_order(self):
        Comment.objects.create(content="Old Comment", post=self.post1, author=self.user)
        Comment.objects.create(
            content="New Comment", post=self.post1, author=self.other_user
        )
        url = reverse("forum:post_detail", args=[self.post1.id])
        response = self.client.get(url)
        content = response.content.decode("utf-8")
        self.assertTrue(content.index("New Comment") < content.index("Old Comment"))

    # TEST CREATE COMMENT (CommentCreateView) #
    def test_comment_create_view_logged_in(self):
        self.client.login(username="otheruser", password="testpass2")
        url = reverse("forum:add_comment", args=[self.post1.id])
        data = {"content": "This is a comment"}
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(content="This is a comment").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Comment added!" in str(m) for m in messages))

    def test_comment_create_view_not_logged_in(self):
        url = reverse("forum:add_comment", args=[self.post1.id])
        data = {"content": "Anon comment"}
        response = self.client.post(url, data, follow=True)
        self.assertNotEqual(response.redirect_chain, [])
        self.assertFalse(Comment.objects.filter(content="Anon comment").exists())

    def test_comment_create_view_invalid(self):
        self.client.login(username="otheruser", password="testpass2")
        url = reverse("forum:add_comment", args=[self.post1.id])
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.exists())

    def test_comment_create_on_non_existing_post(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("forum:add_comment", args=[999])
        data = {"content": "Will fail"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Comment.objects.filter(content="Will fail").exists())

    # TEST UI/FRONTEND #
    def test_ui_elements_on_list(self):
        url = reverse("forum:list")
        response = self.client.get(url)
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(url)
        self.assertContains(response, "Create new post")

    def test_ui_messages_frontend(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("forum:create")
        data = {"title": "UI Test Post", "content": "UI content"}
        response = self.client.post(url, data, follow=True)
        self.assertContains(response, "The post has been created!")


class ForumPermissionsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass2"
        )
        self.post1 = Post.objects.create(
            title="First Post", content="Content of the first post", author=self.user
        )
        self.comment1 = Comment.objects.create(
            content="First comment",
            post=self.post1,
            author=self.other_user,
        )

        self.mod_user = User.objects.create_user(username="moduser", password="modpass")
        moderators_group = Group.objects.create(name="Moderators")
        moderators_group.customuser_set.add(self.mod_user)

        self.client = Client()

    # --- Post DELETE tests ---

    def test_post_delete_by_non_moderator(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("forum:post_delete", args=[self.post1.id])
        response = self.client.post(url, follow=True)

        self.assertTrue(Post.objects.filter(id=self.post1.id).exists())
        self.assertEqual(response.status_code, 403)

    def test_post_delete_by_moderator(self):
        self.client.login(username="moduser", password="modpass")
        url = reverse("forum:post_delete", args=[self.post1.id])
        response = self.client.post(url, follow=True)

        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())
        self.assertIn(response.status_code, [200, 302])

    # --- Comment DELETE tests ---

    def test_comment_delete_by_non_moderator(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("forum:comment_delete", args=[self.comment1.id])
        response = self.client.post(url, follow=True)

        self.assertTrue(Comment.objects.filter(id=self.comment1.id).exists())
        self.assertEqual(response.status_code, 403)

    def test_comment_delete_by_moderator(self):
        self.client.login(username="moduser", password="modpass")
        url = reverse("forum:comment_delete", args=[self.comment1.id])
        response = self.client.post(url, follow=True)

        self.assertFalse(Comment.objects.filter(id=self.comment1.id).exists())
        self.assertIn(response.status_code, [200, 302])
