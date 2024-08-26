# Advanced Django Rest Framework

## Module 1

### Testing

Welcome to Week 1 of the Advanced Django: Advanced Django Rest Framework course. These assignments cover testing the Django rest framework with both mocks and requests. The module ends with graded coding exercises.

Learning Objectives

- Define unit tests
- Create tests with APIClient
- Define the importance of the setup method in tests
- Write tests for GET, PUT, and POST requests
- Write a test to evaluate authentication
- Identify some of the benefits of writing tests with RequestClient
- Write basic authentication and token authentication tests with RequestClient

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

# for Coursera only
# run my test solution
python3 manage.py test_assessment
python3 manage.py test_assessment 2

# test to test my solution
python3 manage.py test
python3 manage.py test assessment.tests_1
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
        self.client.login(email="test@example.com", password="password")
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

## Module 2

Welcome to Week 2 of the Advanced Django: Advanced Django Rest Framework course. These assignments cover optimizing the Django rest framework with caching, throttling, and filtering. The module ends with graded coding exercises.

Learning Objectives

- Apply the cach_page, vary_on_headers, and vary_on_cookie decorators to API views
- Wrap API view caching decorators with @method_decorator
- Add caching to generic views and viewsets
- Vary on both headers and cookies to account for the various ways to authenticate with the API
- Define throttling
- Differentiate between burst and sustained rates
- Identify the periods used for throttling
- Add different throttling for anonymous and authenticated users
- Create different burst and sustained rates for anonymous and authenticated users
- Explain how DRF defines anonymous users
- Scope throttling to different views and viewsets
- Explain what happens to querysets when filtering
- Define user-based filter, url-based filtering, and query parameter filtering
- Add user-based filtering and url-based filtering to Blango

#### Caching Class Method

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CommentListView(APIView):
    @method_decorator(cache_page(60))
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(
            comments, many=True, context={"request": request}
        )
        return Response(serializer.data)
```

We’ve seen how to cache non-generic APIViews, and how to cache action methods on viewsets. But how can we cache the generic APIViews or viewsets when we don’t implement the methods being called?

You will have to implement whichever method you want to cache, and have it just behave as a “pass-through” to the super class’s method.

```python
class UserDetail(generics.RetrieveAPIView):
    # existing methods omitted

    @method_decorator(cache_page(300))
    def get(self, *args, **kwargs):
        return super(UserDetail, self).get(*args, *kwargs)
```

Adding caching to viewsets is similar, except the decorator(s) need to be added to the built-in action methods. Remember from the last course, these methods are: `list()` and `retrieve()`.

You probably don't want to cache updates `create()`, `update()`, `partial_update()` and `destroy()` as they wouldn't do anything.

```python
class PostViewSet(viewsets.ModelViewSet):
    # existing methods omitted

    @method_decorator(cache_page(120))
    def list(self, *args, **kwargs):
        return super(PostViewSet, self).list(*args, **kwargs)
```
