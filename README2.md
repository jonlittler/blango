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
