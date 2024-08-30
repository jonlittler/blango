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

python3 manage.py test assessment.tests_1

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

### Throttling

To prevent resource usage from ballooning out of control, we can implement throttling on our API. That is, limiting the amount of requests that clients can make.

Often, throttling is determined by two different rates, a burst rate and a sustained rate. The burst rate applies over a short period, and the sustained rate over a longer period.

### Filtering

To change the queryset that’s used by the view, we can implement the get_queryset() method. In its default implementation, get_queryset() just returns the queryset attribute.

Filtering on query parameters, access query parameters in `get_queryset()` using the `self.request.query_params` dictionary.

## Module 3

Welcome to Week 3 of the Advanced Django: Advanced Django Rest Framework course. These assignments cover third-party libraries for pagination, tokens, and images. The module ends with graded coding exercises.

Learning Objectives

- Explain the differences between the PageNumberPagination, LimitOffsetPagination, and CursorPagination classes
- Identify differences in the pagination response from the different pagination classes
- Implement pagination on custom action methods
- Install and setup the third-party library django-filter
- Identify the advantage to using the FilterSet class
- Customize the order of results from filtering
- Explain what the JWT library does and why it is beneficial
- Differentiate the access and response tokens from a JWT response
- Identify some of the common settings for JWT
- Add JWT authentication to Blango
- Verify JWT works as expected with Postman
- Explain what django-versatileimagefield does
- Define ppoi
- Add a hero image
- Create a thumbnail image of a specified size
- Add images to a serializer

### Pagination

PageNumberPagination\
Using this class treats the list results as a page, the client can move through the results by specifying a page. `/api/v1/posts/?page=2`

LimitOffsetPagination\
This pagination class works like paginating a SQL query. You would get the first 100 results like this: `/api/v1/posts/?offset=0&limit=100`. Then, fetch the next 100 like this: `/api/v1/posts/?offset=100&limit=100`, and so on.

CursorPagination\
This class uses a special cursor query parameter to page through the results. The parameter is opaque, in that the client doesn’t control it. Instead, on each request, DRF generates URLs containing the cursor variable.

CursorPagination should be considered when working with very large datasets. Paging through data can become slow with using offsets, whereas cursor based paging does not. The disadvantage though, is that a client can’t jump to an arbitrary page or offset.

### THP Django Filter

```bash
pip3 install django-filter
```

```python
INSTALLED_APPS = [ 'django_filters' ]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
}
```

### Simple JTW

```bash
git clone git@github.com:jonlittler/blango.git
```

JWT stands for JSON Web Token. It is a way of encoding authorization information into JSON structure.

JWTs consist of three parts: header, payload and signature. The header consists of a type (usually JWT) and the algorithm (alg) that was used to generate the signature.

The three parts of the JWT, they’re joined together with a . between each component.

https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html

```python
pip3 install djangorestframework-simplejwt PyJWT==1.7.1
```

https://jwt.io/

### Versatile Image Field

`django-versatileimagefield` is a library that provides a drop-in replacement for `ImageField`: `VersatileImageField` (versatileimagefield.fields.VersatileImageField). It provides helper methods to generate thumbnails, crop images, and apply filters.

Along with `VersatileImageField` is `PPOIField` (versatileimagefield.fields.PPOIField), or Primary Point of Interest. This is a field that stores the coordinates of the “point of interest” of the image.

````bash
pip3 install django-versatileimagefield

```python
INSTALLED_APPS = [ 'versatileimagefield' ]
````

## Module 4 JavaScript & React

Welcome to Week 1 of the Advanced Django: Advanced Django Rest Framework course. These assignments cover integrating JavaScript into your Django project. You will assignments on the fundamentals of JavaScript, promises, and React. The module ends with graded coding exercises.

Learning Objectives

- Add a script to a Django template
- Create an alert
- Differentiate between let and const
- Contrast JavaScript objects and Python dictionaries
- Explain the difference between == and ===
- Create a conditional in JavaScript
- Add a comment in JavaScript
- Interact with the console by implementing error, warn, count, log, time, and timeEnd
- Contrast functions in Python and JavaScript
- Create functions using the function keyword, assigning a function to a variable, and using the arrow syntax
- Use setTimeout to wait before running a function
- Create for loops, while loops, do-while loops, and iterate using forEach
- Create a class in JavaScript
- Differentiate constructors between Python and JavaScript
- Use this instead of self in JavaScript classes
- Inherit from a superclass
- Reference the superclass with the super keyword
- Explain the benefit of using an arrow function inside a class
- Define the purpose of promises
- Identify the number of functions needed to implement a promise
- Explain the steps of how a promise is either resolved or rejected
- Invoke a promise and the resolved and rejected callbacks
- Identify the syntax for the or operator in JavaScript
- Define ReactJS
- Add React to a website
- Define React components
- Add a button component that responds to a click
- Mount a component to the DOM
- Define JSX
- Identify when to use double quotes and curly braces with JSX
- Explain the purpose of Babel
- Replace React.createElement with code written in JSX
- Reference information passed to a component with props
- Transform an array of posts into React components
- Define how the fetch function retrieves data
- Transform data from fetch to JSON
- Handle exceptions when using fetch
- Define the three most common React lifecycle methods
- Implement state in a component
- Fetch data when the component mounts
- Pass variables and dictionaries from Django to JavaScript
- Understand how to make the table respond to pagination and sorting

### JS Intro

```bash
git clone git@github.com:jonlittler/blango.git
```

### JS Functions

```js
const addNumber = function (a, b) {
  return a + b;
};
const addNumber = (a, b) => {
  return a + b;
};
```

### JS Classes

```js
class Car extends Vehicle {
  constructor(make, model) {
    this.make = make;
    this.model = model;
  }
}
```

### JS Promises

The purpose of promises is to provide a method of performing asynchronous code, or running code in the background. Since JavaScript doesn’t have a threading model, this is accomplished with callbacks.

Promises work because functions can be passed around in JavaScript. We need at least two, and sometimes three functions to implement a Promise.

The first is the function that actually does the work. Rather than return a result, the worker function will call a function with the result, to “resolve” the promise.

If there’s a failure in the worker function, then it might also be able to “reject” the promise.

```js
// Producer Side of Promise

const lazyAdd = function (a, b) {
  const doAdd = (resolve, reject) => {
    if (typeof a !== "number" || typeof b !== "number") {
      reject("a and b must both be numbers")
    } else {
      const sum = a + b
      resolve(sum)
    }
  }

  return new Promise(doAdd)
```

The function that other code will call is `lazyAdd`, but we define another function inside it called `doAdd` which contains the actual code to do the addition.

We need to do this because the function we pass to the Promise class must only take resolve and reject functions as parameters. We could not pass a function to Promise that takes the numbers to add and the resolve and reject functions.

By wrapping `doAdd()`, it has access to the parent function’s variables, and so it can access the `a` and `b` parameters.

```js
// Executor Side of Promise

function resolvedCallback(data) {
  console.log("Resolved with data: " + data);
}

function rejectedCallback(message) {
  console.log("Rejected with message: " + message);
}

// p is a Promise instance that has not yet been settled
// There will be no console output at this point.
const p = lazyAdd(3, 4);

// This next line will settle the doAdd function
// There will be some console output now
p.then(resolvedCallback, rejectedCallback);
```

### React JS

```js
// Create Element

class ClickButton extends React.Component {
  state = { wasClicked: false };
  handleClick() {
    this.setState({ wasClicked: true });
  }

  render() {
    let buttonText;

    if (this.state.wasClicked) buttonText = "Clicked!";
    else buttonText = "Click Me";

    return React.createElement(
      "button",
      {
        className: "btn btn-primary mt-2",
        onClick: () => {
          this.handleClick();
        },
      },
      buttonText
    );
  }
}

// Mount to DOM

const domContainer = document.getElementById("react_root");
ReactDOM.render(React.createElement(ClickButton), domContainer);
```

### JSX

#### Babel

Babel is a tool that, among other things, compiles JSX to JavaScript. It can also compile JavaScript that uses new features into JavaScript that’s compatible with older browsers, so it’s a useful tool to know about.

Since we just have a single JavaScript file to compile, we’re going to use a simple method. It’s not as fast as pre-compiling everything, but for our use case we probably won’t notice a difference.

There are two steps to get Babel set up in this way.

First, we need to include the Babel script, before we include any of our own JavaScript that needs to be compiled:

```js
<script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
```

Then we need to add the attribute type="text/babel" to any `<script>s` that we want to be compiled. For example:

```js
<script type="text/babel" src="{% static "blog/blog.js" %}"></script>
```
