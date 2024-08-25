# Intro to REST API

## Module 1

Welcome to Week 1 of the Advanced Django: Introduction to Django Rest Framework course. These assignments cover RESTful APIs, the first-party Django REST API, and Postman. The module ends with graded coding exercises.

Learning Objectives

- Explain why having raw data in a structured format is beneficial
- Define REST API
- Explain how GET, POST, PUT, and DELETE work with the Post pattern
- Explain how GET, POST, PUT, and DELETE work with the Post ID pattern
- Explain the importance of the JsonResponse and HttpResponse classes
- Transform a model into data that is serializable
- List all Post objects in a view
- List all Post details in a view
- Create URL paths for the new views
- Explain the purpose of Postman
- Install Postman on your computer
- Create a Postman variable that has the base URL for testing
- Perform GET, PUT, POST, and DELETE requests with Postman
- Identify the limitations of this primitive API

## Module 2

Welcome to Week 2 of the Advanced Django: Introduction to Django Rest Framework course. These assignments cover serializers and views. The module ends with graded coding exercises.

Learning Objectives

- Explain the benefits of Django Rest Framework
- Define the role of a serializer
- Create a serializer for the User model
- Hide passwords when creating serializers
- Deserialize JSON data
- Raise an exception when serializing invalid data
- Create objects from validated data
- Serialize and deserialize multiple objects at once
- Provide custom validation with field-level validation and validator functions
- Differentiate a ModelSerializer from a Serializer
- Add a ModelSerializer for the Post model
- Decorate a view function to become an API method
- Load the API in the DRF GUI
- Add ability to look at the JSON of API objects
- Contrast a class-based view with a function-based view
- Explain how generic views reduce the amount of code
- Create generic views for the PostList and PostDetail classes

### Serializers

https://www.django-rest-framework.org/api-guide/fields/

```bash
pip3 install djangorestframework
python3 manage.py shell
```

```python
from django.utils import timezone
from rest_framework import serializers

class User:
    def __init__(self, username, email=None, first_name=None, last_name=None, password=None, join_date=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.join_date = join_date or timezone.now()

def is_capitalized(value):
    if value[0].lower() == value[0]:
        raise serializers.ValidationError("value must be capitalized")

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=20, required=False, validators=[is_capitalized])
    last_name = serializers.CharField(max_length=20, required=False, validators=[is_capitalized])
    password = serializers.CharField(write_only=True, required=False)
    join_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return User(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance

    def validate_email(self, value):
        value = value.lower()
        domain = value.split("@")[1]
        if domain != "jonlittler.com":
            raise serializers.ValidationError("domain must be jonlittler.com")
        return value

    def validate(self, data):
        if (not data.get("first_name")) != (not data.get("last_name")):
            raise serializers.ValidationError("first_name and last_name must be provided together")
        return data

# valid
u2 = {"username": "apple", "join_date": "2024-08-23T11:11:11.123412Z"}
s2 = UserSerializer(data=u2)
s2.initial_data
s2.is_valid()
s2.data
s2.validated_data

# error
u3 = {"username": "pjlonglastname", "first_name": "Pj", "last_name": "This Is 26 Characters Long", "some_other_key": "extra"}
s3 = UserSerializer(data=u3)
s3.initial_data
s3.is_valid()
s3.data
s3.validated_data
s3.errors
s3.is_valid(raise_exception=True)

# save
user_data = {"username": "paj", "first_name": "Pj", "last_name": "Apple"}
serializer = UserSerializer(User, data=user_data)
serializer.is_valid()
u1 = serializer.save()
u1.first_name

# validation
u4 = UserSerializer(data={"username": "paj2", "email": "paj@notjonlittler.com"})
u4.is_valid()
u4.errors

u5 = UserSerializer(data={"username": "paj2", "first_name": "paj", "email": "paj@jonlittler.com"})
u5.is_valid()
u5.errors
```

## Module 3

Welcome to Week 3 of the Advanced Django: Introduction to Django Rest Framework course. These assignments cover authentication, permissions, related fields, and nested relationships. The module ends with graded coding exercises.

Learning Objectives

- Explain the importance of authentication
- Define session authentication
- Add session authentication to Blango
- Contrast basic authentication from session authentication
- Authenticate with Postman, your username, and your password
- Identify the benefits of token authentication
- Add token authentication to Blango
- Define the purpose of permissions
- Identify some common permissions
- Update Blango so only authenticated users can make changes
- Use custom permissions to restrict access to objects
- Combine permissions so that only the author or admin users can make changes
- Identify the benefits from having related fields
- Define PrimaryKeyRelatedField, StringRelatedField, SlugRelatedField, and HyperlinkRelatedField
- Add a SlugRelatedField for tags to the PostSerializer class
- Add a HyperlinkRelatedField for the author to the - PostSerializer class
- Define a read-only nested relationship
- Define a read-write nested relationship
- Implement an update method to avoid a race condition
- Use the get_or_create method to automatically create related objects
- Modify Blango to create and see comments through the API
- Modify Blango to create tags through the API

When dealing with user access to the API, there are actually two pieces: authentication, which is who you are; and permissions, which is what you are allowed to do.

### Authentication

https://chariotgizmo-dealinvite-8000.codio.io/api/v1/posts
https://chariotgizmo-dealinvite-8000.codio.io/admin
https://chariotgizmo-dealinvite-8000.codio.io/accounts/login

#### Session

The standard way of authenticating in Django, is to log in with a username and password using a form. This user information is then stored in the session, on the backend. The session is identified by a cookie sent by the browser.

Using session authentication is not ideal for use with an API. With a REST API it’s useful for the client to be able to tell who the current user is, by looking at the request.

#### Basic Authentication

Basic authentication is more useful than session authentication when it comes to REST APIs. Basic authentication involves sending the username and password with each request.

`Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=`

dXNlcm5hbWU6cGFzc3dvcmQ= being the string username:password encoded by base-64.

```bash
python3 blango/manage.py shell
```

```python
import requests
from requests.auth import HTTPBasicAuth

# basic
requests.get("https://chariotgizmo-dealinvite-8000.codio.io/api/v1/posts/", auth=HTTPBasicAuth("user@example.com", "badpassword"))

# token
requests.get("http://127.0.0.1:8000/api/v1/posts/", headers={"Authorization": "Token 81082614a73f331b122ba93dbdb5951b44cf21d4"})
```

#### Token Authentication

Token authentication works by passing a token (a long, random string) in the Authorization header.

`Authorization: Token fccdf7307189644e9fee624224d3471d870a7b829f5c23d0297f15e34c41b974`

`Authorization: Bearer fccdf7307189644e9fee624224d3471d870a7b829f5c23d0297f15e34c41b974`

To use token authentication in DRF we need to add token authorization as an installed app and the authentication classes in the `settings.py` file.

```python
INSTALLED_APPS = [
    rest_framework.authtoken
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ]
}
```

To apply django rest framework token authentication, you must run a migrate after updating `settings.py`.

```bash
python3 manage.py migrate
```

BasicAuthentication & SessionAuthentication are provided by default,however, need to be included when adding TokenAuthentication.

**Four** options to create a token:

1. Through Code

```python
from blango_auth.models import User
from rest_framework.authtoken.models import Token

u = User.objects.get(pk=1)
u.email # 'ben@example.com'

t = Token.objects.create(user=u)
t.key   # '81082614a73f331b122ba93dbdb5951b44cf21d4'
```

2. Through Django Admin

https://chariotgizmo-dealinvite-8000.codio.io/admin/authtoken/tokenproxy/add/

3. Through manage.py

```bash
$ python3 manage.py drf_create_token pj@jonlittler.com
```

4. Through DRF (api/urls.py)

POST JSON @ https://chariotgizmo-dealinvite-8000.codio.io/api/v1/token-auth/

```python
from rest_framework.authtoken import views
```

### Permissions

Django Rest Framework provides a few helpful classes to add common types of permissions restrictions to views. They’re all importable from `rest_framework.permissions`.

### Related Fields

#### Primary Key

_PrimaryKeyRelatedField_ is actually what we’ve been using so far, the DRF ModelSerializer class sets it up automatically for us behind the scenes. When PostSerializer serializes an author or tags, it renders the related model’s primary key field.

```python
# this id by default
author = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
tags = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
```

#### String Key

_StringRelatedField_ is a serializer field that calls the `__str__()` method of the related object that’s being serialized.

```python
tags = serializers.StringRelatedField(many=True)
```

#### Slug Key

_SlugRelatedField_ is intended to work with a SlugField of a related object, although it can work with any unique field.

```python
tags = serializers.SlugRelatedField(slug_field="value", many=True, queryset=Tag.objects.all())
```

#### Hyperlink

_HyperlinkRelatedField_ field serializes a related object to a URL at which we can retrieve the full detail of the object. It requires the name of a view to be provided, and this is used to generate the URL by passing in the primary key of the related object.

```python
# will need a
# - UserSerializer
# - UserDetail view
# - users/<int:pk> or users/<str:email> url

author = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name="api_user_detail")
```
