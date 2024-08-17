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
