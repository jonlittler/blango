# blango

## Module 1

Welcome to Week 1 of the Advanced Django: Building a Blog course. These assignments cover creating a blog in Django, generic relationships, the Bootstrap HTML framework, filters, tags, and crispy forms. The module ends with graded coding exercises.

Learning Objectives

- Setup a blog application in Django
- Configure the dev server to run inside the Codio platform
- Run database migrations
- Create the Tag and Post models
- Register the Tag and Post models with Django Admin
- Create a post through Django Admin
- Identify limitations of not using generic relationships
- Dynamically access models using the contenttypes framework
- Create generic relationships between different models
- Use GenericRelation for reverse queries
- Create the Comment model with a generic relationship to the Post model
- Add the Bootstrap framework to a Django project
- Insert the following components into a Django project: Alerts, - Buttons, Dropdowns, Modal, NavBar, Pagination
- Add a container to the <body> element
- Change the default width of the container
- Create columns within the container
- Manually set the width of a column
- Set the width of a column relative to a breakpoint
- Use built-in filters in a Django template
- Create custom template tags for the posts
- Create a custom filter and add it to a template
- Render text safe to increase the security of the blog
- Pass an argument to a filter
- Identify why custom template tags can be better than filters
- Create a simple tag
- Add context to a custom template tag
- Use a template inside another template with inclusion tags
- Identify when to use an advanced template tag
- Render a Django form
- Setup a Django project to use Crispy Forms
- Use Crispy on an existing form
- Use FormHelper to customize a form
- Simplify a form with the crispy template tag

Starting point for the Advanced Django course. This is the equivalent of the following command:

```bash
$ django-admin.py startproject blango
```

### Generic Relationships Content Types

`python manage.py shell`

```python
from django.contrib.contenttypes.models import ContentType
from blog.models import Post

post_type = ContentType.objects.get(app_label="blog", model="post")
post_type
post_type.model_class()
post_type.get_object_for_this_type(pk=1)    # shortcut method
post_type.model_class().objects.get(pk=1)

post_type.get_object_for_this_type(pk=1) == post_type.model_class().objects.get(pk=1)

ContentType.objects.all()
ContentType.objects.get_for_model(Post)
```

By utilizing `ContentType` we can allow a model to be related to any number of models by just adding three attributes to a Model:

1. A `ForeignKey` field that points to a `ContentType`. Normally this is called content_type
2. A `PositiveIntegerField` that stores the primary key of the related object. Normally this is called object_id
3. A `GenericForeignKey` field, a special type of field that will look up the object from the other two new fields.

#### Commenting on a Post / User

`python manage.py shell`

```python
from blog.models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

p = Post.objects.first()
u = User.objects.first()

c1 = Comment(creator=u, content="What a great post!", content_object=p)
c1.save()
c1.content_object

c2 = Comment(creator=u, content="I like myself!", content_object=u)
c2.save()
c2.content_object

p.comments.all()
c3 = p.comments.all()[0]
p.comments.remove(c3)
p.comments.all()
```

### Bootstrap Setup

```html
<link
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
  rel="stylesheet"
  integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcgQTwFspd3yD65VohhpuuCOmLASjC"
  crossorigin="anonymous" />

<link
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
  rel="stylesheet"
  integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
  crossorigin="anonymous" />
```

### Simple Filter Tag

In its simplest form, a filter is just a function that takes a single argument and returns a string to be rendered in the template.

> By default, Django will escape the return value. In order to render it as HTML, use `format_html`.

- create `blog/templatetags` folder
- add empty `__init__.py`
- add blogs_extra.py

Before the filter can be used, it needs to be registered into the template library. This is actually a three step process:

1. Import the django template module.
2. Create an instance of the `django.template.Library` class.
3. Register the filter function into the `Library` with its `filter` function.

### Templates

- Variable `{{ first_name }}`

- Tag `{% csrf_token %}`

The `{% for %}` tag can take an optional `{% empty %}` clause whose text is displayed if the given array is empty or could not be found.

### Crispy Forms

Since `crispy-bootstrap5` depends on `django-crispy-forms`, you only need to install `crispy-bootstrap5` with `pip` and `django-crispy-forms` will be installed automatically.

```bash
pip3 install crispy-bootstrap5
```

Open settings.py

1. Add `"crispy_forms"` and `"crispy_bootstrap5"` to your `INSTALLED_APPS`.
2. Add the setting `CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"`.
3. Finally, add the setting `CRISPY_TEMPLATE_PACK = "bootstrap5"`.

## Module 2

Welcome to Week 2 of the Advanced Django: Building a Blog course. These assignments cover 12 factor apps, configuring Django, logging, security, and hosting. The module ends with graded coding exercises.

Learning Objectives

- Identify the importance of 12 Factor Apps
- Define each of the 12 factors
- Define environment variable
- Reference, set, and override environment variables
- Use environment variables to configure your Django project
- Identify the different logging levels
- Add a logger to your Django project
- Use a formatter to provide more context to logging messages
- Identify import logging concepts that go beyond 12 Factor Apps
- Identify the ways in which Django is secure by default
- Define hashing and explain why it is important
- Define salting
- Explain how Django stores passwords
- Define the different methods of production hosting
- Explain the pros and cons of each production hosting method
- Describe the different factors that you should consider when selecting a hosting solution

### 12 Factors

1. Codebase - a single source repository
2. Dependencies - requirements.txt
3. Config - environment variables \*\*
4. Backing Services - database abstraction
5. Build, Release & Run
6. Processes - stateless, data stored in db
7. Port Binding - expose interface on a specific tcp port
8. Concurrency - horizontal scaling
9. Disposability - restart quickly with no data loss
10. Dev/Prod Parity - consistent tools and versions
11. Logs - write to stdout \*\*
12. Admin - one off on production

### Environment

```python
from os import environ
environ.setdefault("MY_VAR1", "Hello from PAJ")
print(f"Message: {environ["MY_VAR1"]}")
```

### Django Configurations

```bash
pip3 install django-configurations dj-database-url

# set timezone env
DJANGO_TIME_ZONE="Europe/London" python3 manage.py runserver 0.0.0.0:8000
BLANGO_TIME_ZONE="Europe/London" python3 manage.py runserver 0.0.0.0:8000

# database url
mysql://username:password@mysql-host.example.com:3306/db_name?option1=value1&option2=value2

# /// empty hostname
sqlite:///{BASE_DIR}/db.sqlite3
```

There are a couple of things to be aware of when using `DatabaseURLValue`. It differs from the other Value classes in that it doesn’t read the value from the environment variable `DJANGO_DATABASES`, as you would expect from the convention seen so far. Instead, it reads from the environment variable `DATABASE_URL`.

### Logging

- Loggers - name and level
- Handlers - where to log the message
- Filters - drop messages
- Formatters - add meta data e.g., date and time

Default security level is `WARNING`, so the logging module will not log messages with `DEBUG` and `INFO`.

https://docs.python.org/3.9/library/logging.handlers.html

### Security

pbkdf2_sha256$260000$ud2D0L3h8b98JDjGaffUnQ$LAYlrboOAUGZdRhEh7xT/oom2Nv/dpJpmDOpnmPze0k= \

`algorithm`\$`iterations`\$`salt`\$`hash` \
algorithm = pbkdf2_sha256 \
iterations = 260000 \
salt = ud2D0L3h8b98JDjGaffUnQ \
hash = LAYlrboOAUGZdRhEh7xT/oom2Nv/dpJpmDOpnmPze0k= \

```bash
pip install --upgrade setuptools
pip install "django[argon2]"
```

## Module 3

Welcome to Week 3 of the Advanced Django: Building a Blog course. These assignments cover increasing performance by caching and optimizing the database. The module ends with graded coding exercises.

Learning Objectives

- Explain how caching speeds up performance
- Identify different ways to cache data in Django
- Add view caching to different views
- Adjust the time for which views are cached
- Vary caching based on cookies
- Cache only specific parts of a template
- Perform lower level caching actions
- Use Django Debug Toolbar to monitor performance
- Implement database indexes to speed up finding records
- Use select_related to fetch all of the data in one query
- Use bulk operations (create, update, delete) to reduce the number of queries

### Cache

https://docs.djangoproject.com/en/3.2/topics/cache/

#### Memcached

```bash
sudo apt install memcached
```

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION"": "127.0.0.1:11211",
    }
}
```

#### Database

```bash
python manage.py createcachetable
```

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "my_cache_table",
    }
}
```

#### Filesystem

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
    }
}
```

#### Local Memory

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
```

#### Dummy

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
```

#### Shell

```bash
python3 manage.py shell
```

```python
from django.core.cache import caches
default_cache = caches["default"]

# or

from django.core.cache import cache
# cache is the equivalent of caches["default"]/our default_cache variable

from django.core.cache import cache
from blog.models import Post

post_pk = 1
p = Post.objects.get(pk=post_pk)
cache.set(f"post_{post_pk}", p, 30) # 30 secs

p1 = cache.get(f"post_{post_pk}")
p == p1

# wait 30 secs
print(cache.get(f"post_{post_pk}"))

# or delete key
cache.delete(f"post_{post_pk}")

# default using sentinel
sentinel = object()
cache.set("current_user", None, 30)
u = cache.get("current_user", sentinel)
u is None       # True
u is sentinel   # False

# wait 30 secs
u = cache.get("current_user", sentinel)
u is sentinel   # True
```

```bash
python3 manage.py shell
```

```python
from django.core.cache import cache
from blog.models import Post

# cache many
all_posts = Post.objects.all()
posts_to_cache = {f"post_{post.pk}": post for post in all_posts}
posts_to_cache
cache.set_many(posts_to_cache, 30)

# get / get many
cache.get("post_2")
cache.get_many(["post_1", "post_2", "post_1000"])

# None Null
cache.set("none_value", None, 30)
# {'none_value': None}

cache.get_many(["none_value"])
# after 30 secs {}

# delete many
# get or set many
cache.set("key1", "value1")
cache.get_or_set("key1", "value2")      # 'value1'
cache.get_or_set("key2", "value3")      # 'value3'
cache.get_or_set("key2", "value4")      # 'value3'
```

### Explain Queryset

```bash
python3 manage.py shell
```

```python
from blog.models import Post
Post.objects.first().comments.explain()
# 0 0 0 SEARCH TABLE blog_comment USING INDEX blog_comment_content_type_id_e26f0063 (content_type_id=?)

# after index on object_id & created_at
# 0 0 0 SEARCH TABLE blog_comment USING INDEX blog_comment_object_id_134c93ed (object_id=?)
```

### Bulk DB Operations

https://docs.djangoproject.com/en/3.2/topics/db/optimization/

```bash
python3 manage.py shell
```

```python
from blog.models import Post, Comment

# bulk create
comments = []
for post in Post.objects.all():
    comments.append(
    Comment(creator=post.author, content="Thank you for reading my post!", content_object=post))
Comment.objects.bulk_create(comments)

# bulk update
comments = Comment.objects.filter(content="Thank you for reading my post!")
for comment in comments:
    comment.content = comment.content + " Signed, " + comment.creator.username
Comment.objects.bulk_update(comments, ["content"])

# bulk delete
Comment.objects.filter(content__contains="Thank you for reading my post!").delete()
```

## Module 3

Welcome to Week 4 of the Advanced Django: Building a Blog course. These assignments cover creating a custom user model, Django registration, and Django Allauth. The module ends with graded coding exercises.

Learning Objectives

- Explain why it is better to use a custom User model from the beginning
- Create a custom User model
- Identify when to use a custom model or a separate model
- Change authentication from username to email
- Differentiate between one-step and two-step activation
- Add login page and a profile users see once logged in
- Create two-step activation for your blog
- Send users an activation email
- Set a window for which users must activate their account
- Remove users who have not activated their accounts
- Describe the Django Allauth library
- Create a Google project through their developer portal
- Allow users to sign in with their Google credentials with Allauth
- Set up Google app credentials as a SocialApp

### Custom User Model

https://docs.djangoproject.com/en/5.0/topics/auth/customizing/

Set up your own User model when you start your project, it’s fairly simple.

1. Create a user model that inherits from `django.contrib.auth.model.AbstractUser` (it doesn’t need to be called User). This can be in any app in your project, but you should consider creating an app just for authentication-related models, templates, forms and views.
2. Add the `AUTH_USER_MODEL` setting to point to the new Model. If you’ve added the model inside a new app, make sure to add that to `INSTALLED_APPS`.
3. Register the Model in the `admin.py` for the app in which it was created.

#### Dump Data of existing user model

```bash
# backup data
python3 manage.py dumpdata -o data.json blog.Comment blog.Tag blog.Post auth.User

# create user app
python3 manage.py startapp blango_auth

# load data
python3 manage.py loaddata data.json
```

Adding a model means the content type IDs have changed, so we’ll need to update all the Comment objects to point to the new content type of Post.

```python
from django.contrib.contenttypes.models import ContentType
from blog.models import Comment, Post
post_type = ContentType.objects.get_for_model(Post)
Comment.objects.update(content_type=post_type)
```

### Email Authentication

To implement email login we need to do the following:

- Create a new `UserManager` subclass, and override the `create_user()` and `create_superuser()` methods. We need to have the methods require an email address instead of a username.
- Update the `User` model to make the email field unique and remove the `username` field.
- Set the `User` model’s objects attribute to an instance of the new user manager.
- Set the `User` model’s `USERNAME_FIELD` to "email".
- Set the `User` model’s `REQUIRED_FIELDS` to an empty list. This might seem strange, because by default this value is `["email"]`, however Django assumes the `USERNAME_FIELD` is required, and so doesn’t allow it to be listed in `REQUIRED_FIELDS`.
- Change the `__str__()` method of User to return the email address.
  Subclass django.contrib.auth.admin.UserAdmin and remove any reference to username or replace with email.

> What does \_("email address") mean?

The first positional argument for an EmailField is the label. The method `_()` is typically `gettext_lazy` or `gettext` but aliased to `_`.

This is done via (specific example in the docs 2):

```python
from django.utils.translation import gettext_lazy as _
```

The function gettext_lazy is used to support internationalization of text.
