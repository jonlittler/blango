from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from pytz import UTC
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from blog.models import Post
import logging

class PostApiTestCase(TestCase):

  def setUp(self):

    # Creates two test users and assigns them to self.u1 and self.u2
    self.u1 = get_user_model().objects.create_user(
      email="test@example.com", password="password")

    self.u2 = get_user_model().objects.create_user(
      email="test2@example.com", password="password2")

    # Creates two Post objects.
    posts = [
      Post.objects.create(
        author=self.u1,
        published_at=timezone.now(),
        title="Post 1 Title",
        slug="post-1-slug",
        summary="Post 1 Summary",
        content="Post 1 Content" ),
      Post.objects.create(
        author=self.u2,
        published_at=timezone.now(),
        title="Post 2 Title",
        slug="post-2-slug",
        summary="Post 2 Summary",
        content="Post 2 Content" ),
    ]

    # Let's us look up the post info by ID
    self.post_lookup = {p.id: p for p in posts}

    # Override test client
    self.client = APIClient()

    # Inserts a Token object into the database
    token = Token.objects.create(user=self.u1)

    # Sets the credentials() of the APIClient client
    self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    # Set logging level to avoid 404 WARNING
    logger = logging.getLogger('django.request')
    logger.setLevel(logging.ERROR)

  def tear_down(self):
    logger = logging.getLogger('django.request')
    logger.setLevel(logging.WARNING)

  def test_post_list(self):
    resp = self.client.get("/api/v1/posts/")
    data = resp.json()["results"]
    self.assertEqual(len(data), 2)

    for post_dict in data:
      post_obj = self.post_lookup[post_dict["id"]]
      self.assertEqual(post_obj.title, post_dict["title"])
      self.assertEqual(post_obj.slug, post_dict["slug"])
      self.assertEqual(post_obj.summary, post_dict["summary"])
      self.assertEqual(post_obj.content, post_dict["content"])
      self.assertTrue(
        post_dict["author"].endswith(f"/api/v1/users/{post_obj.author.email}"))
      self.assertEqual(
          post_obj.published_at,
          datetime.strptime(
              post_dict["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
          ).replace(tzinfo=UTC))

  def test_unauthenticated_post_create(self):
    # Unset credentials so we are an anonymous user
    self.client.credentials()

    # Create dummy POST
    post_dict = {
      "title": "Test Post",
      "slug": "test-post-3",
      "summary": "Test Summary",
      "content": "Test Content",
      "author": "http://testserver/api/v1/users/test@example.com",
      "published_at": "2021-01-10T09:00:00Z"}

    # Attempt POST
    resp = self.client.post("/api/v1/posts/", post_dict)
    self.assertEqual(resp.status_code, 401)
    self.assertEqual(Post.objects.all().count(), 2)

  def test_post_create(self):
    # Create dummy POST
    post_dict = {
      "title": "Test Post",
      "slug": "test-post-3",
      "summary": "Test Summary",
      "content": "Test Content",
      "author": "http://testserver/api/v1/users/test@example.com",
      "published_at": "2024-08-26T11:11:00Z",
    }
    # Attempt POST
    resp = self.client.post("/api/v1/posts/", post_dict)

    # Retrieve POST from database
    post_id = resp.json()["id"]
    post = Post.objects.get(pk=post_id)

    # Assert
    self.assertEqual(post.title, post_dict["title"])
    self.assertEqual(post.slug, post_dict["slug"])
    self.assertEqual(post.summary, post_dict["summary"])
    self.assertEqual(post.content, post_dict["content"])
    self.assertEqual(post.author, self.u1)
    self.assertEqual(post.published_at, datetime(2024, 8, 26, 11, 11, 0, tzinfo=UTC))
