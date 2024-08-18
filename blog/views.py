from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_headers

from blog.models import Post
from blog.forms import CommentForm

import logging

# Create your views here.

logger = logging.getLogger(__name__)

# @cache_page(300)
# @vary_on_headers("Cookie")
def index(request):

  # from django.http import HttpResponse
  # return HttpResponse(str(request.user).encode("ascii"))

  posts = Post.objects.filter(published_at__lte=timezone.now())
  logger.debug("Got %d posts", len(posts))
  return render(request, "blog/index.html", {"posts": posts})

def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)

  if request.user.is_active:
    if request.method == "POST":
      comment_form = CommentForm(request.POST)  # save comment
      if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.content_object = post
        comment.creator = request.user
        comment.save()  # link comment to post and user

        logger.info("Created comment on Post %d for user %s", post.pk, request.user)
        return redirect(request.path_info)
    else:
      comment_form = CommentForm()  # blank form
  else:
    comment_form = None # must be logged into to comment

  return render(request, "blog/post-detail.html", {"post": post, "comment_form": comment_form})
