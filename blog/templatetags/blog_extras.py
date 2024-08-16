from django import template
from django.contrib.auth import get_user_model
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from blog.models import Post

register = template.Library()
user_model = get_user_model()

# Template Filter (|author_details:request.user)
@register.filter(name='author_details')
def author_details(author, current_user=None):
  if not isinstance(author, user_model):
    return ''

  if author == current_user:
    return format_html('<strong>me</strong>')                   # safe

  if author.first_name and author.last_name:
    name = f'{author.first_name} {author.last_name}'
  else:
    name = f'{author.username}'

  if author.email:
    prefix = format_html('<a href="mailto:{}">', author.email)  # safe
    suffix = format_html('</a>')                                # safe
  else:
    prefix = ""
    suffix = ""

  return format_html('{}{}{}', prefix, name, suffix)            # safe

#Template Tags (row, col & endrow)
@register.simple_tag(name='row')
def row(extra_classes=''):
  return format_html('<div class="row {}">', extra_classes)

@register.simple_tag(name='endrow')
def endrow():
  return format_html("</div>")

#Template Tags (col & endcol)
@register.simple_tag(name='col')
def col(extra_classes=''):
  return format_html('<div class="col {}">', extra_classes)

@register.simple_tag(name='endcol')
def endcol():
  return format_html("</div>")

# Template Tag (author_details_tag)
@register.simple_tag(name='author_details_tag', takes_context=True)
def author_details_tag(context):

  # extract variables (current user & author) from context
  request = context["request"]
  post = context["post"]
  current_user = request.user
  author = post.author

  if author == current_user:
    return format_html('<strong>me</strong>')                   # safe

  if author.first_name and author.last_name:
    name = f'{author.first_name} {author.last_name}'
  else:
    name = f'{author.username}'

  if author.email:
    prefix = format_html('<a href="mailto:{}">', author.email)  # safe
    suffix = format_html('</a>')                                # safe
  else:
    prefix = ""
    suffix = ""

  return format_html('{}{}{}', prefix, name, suffix)            # safe

# Inclusion Tag

@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
  posts = Post.objects.exclude(pk=post.pk)[:5]
  return {"title": "Recent Posts", "posts": posts}
