# Advanced Django Rest Framework

## Testing

```bash
git clone git@github.com:jonlittler/blango.git
```

Unit tests are normally grouped into test cases, represented by a TestCase subclass.

The actual validation of results is done using assertions. TestCase provides a number of assertion methods that can be called for various checks.

For example, `assertEqual()`, `assertNotEqual()`, `assertTrue()`, `assertFalse()`, `assertIn()` (for example, check if an item is in a list or dictionary), `assertNotIn()` (the opposite), and more.

If you can’t find an assertion you need, you can always fall back to writing a test and wrapping it in `assertTrue()`.

#### Run Tests

```python
python3 manage.py test  # run all tests
python3 manage.py test blog.test_post_api
python3 manage.py test blog.test_tag_api
```

#### Example GET

Decode with json().

```python
class RestTestCase(TestCase):
    def test_post_list(self):
        resp = self.client.get("/api/v1/posts/")
        data = resp.json()
        self.assertIsInstance(data, list)
```

#### Example POST

Encode with json.dump().

```python
class RestTestCase(TestCase):
    def test_post_create(self):
        resp = self.client.post(
            "/api/v1/posts/",
            json.dumps({"content": "Post Content", "slug": "post-slug", ...}),
            HTTP_AUTHORIZATION="Token abc1234def567",
            content_type="application/json",
        )
        data = resp.json()
        self.assertEqual(data["slug"], "post-slug")

# -or

    def test_post_create(self):
        post_dict = {
            "title": "Test Post",
            "slug": "test-post-3",
            "summary": "Test Summary",
            "content": "Test Content",
            "author": "http://testserver/api/v1/users/test@example.com",
            "published_at": "2021-01-10T09:00:00Z"
        }
        resp = self.client.post("/api/v1/posts/", post_dict)

        post_id = resp.json()["id"]
        post = Post.objects.get(id=post_id)
        self.assertEqual(post.slug, post_dict["slug"])
```

#### Advances Request Factory (to review only)

https://docs.djangoproject.com/en/3.2/topics/testing/advanced/#django.test.client.RequestFactory

### Authentication

#### Session

Most of the time, if you're going to be testing or using an API you won't be doing so with session based authentication. Using the session for authentication is normally only used for GUIs in browsers.

```python
class PostApiTestCase(TestCase):
    def test_post_creation(self):
        self.client.login(email="test@example.com", password="test@example.com")
        self.client.post("/api/v1/posts/", {"content": ...})
```

#### Basic

```python
import base64

credentials = base64.b64encode("test@example.com:password".encode("ascii"))
auth_header = "Basic " + credentials.decode("ascii")
```

#### Token

```python
token = "4510a3fdd351d2a35059e9724fa4bdbb643f4325cd8f6696298f80efbaf4d2c9"
auth_header = "Token " + token
client.credentials(HTTP_AUTHORIZATION=auth_header)
```

Create user token in `setup()` step is preferred. Create user, generate token and then save to database.

```python
class PostApiTestCase(TestCase):
    def setUp(self):
        self.u1 = get_user_model().objects.create_user(
            email="test@example.com", password="password"
        )

        self.client = APIClient()
        token = Token.objects.create(user=self.u1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
```
