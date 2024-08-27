from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.api.serializers import PostSerializer, PostDetailSerializer
from blog.api.serializers import UserSerializer
from blog.api.serializers import TagSerializer
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject

from blog.models import Post, Tag
from blango_auth.models import User

# Caching imports
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

from rest_framework.exceptions import PermissionDenied

# Queryset filtering
from django.db.models import Q
from django.utils import timezone
from django.http import Http404
from datetime import timedelta

# thp filtering
from blog.api.filters import PostFilterSet


# class PostList(generics.ListCreateAPIView):
#   queryset = Post.objects.all()
#   serializer_class = PostSerializer


# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#   queryset = Post.objects.all()
#   serializer_class = PostDetailSerializer
#   # permission_classes = [AuthorModifyOrReadOnly]
#   permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]


class UserDetail(generics.RetrieveAPIView):
  lookup_field = "email"
  queryset = User.objects.all()
  serializer_class = UserSerializer

  # Override User get (this is a view), so that can cache for 5 minutes
  @method_decorator(cache_page(300))
  def get(self, *args, **kwargs):
    return super(UserDetail, self).get(*args, *kwargs)


class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

  @action(methods=["get"], detail=True, name="Posts with the Tag")
  def posts(self, request, pk=None):
    tag = self.get_object()

    # manual pagination
    page = self.paginate_queryset(tag.posts)
    if page is not None:
      post_serializer = PostSerializer(page, many=True, context={"request": request})
      return self.get_paginated_response(post_serializer.data)

    post_serializer = PostSerializer(tag.posts, many=True, context={"request": request})
    return Response(post_serializer.data)

    # Override Tag list (this is a viewset), so that can cache for 5 minutes
    @method_decorator(cache_page(300))
    def list(self, *args, **kwargs):
      return super(TagViewSet, self).list(*args, **kwargs)

    # Override Tag retrieve (this is a viewset), so that can cache for 5 minutes
    @method_decorator(cache_page(300))
    def retrieve(self, *args, **kwargs):
      return super(TagViewSet, self).retrieve(*args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
  permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]

  # thp filters, ordering
  # filterset_fields = ["author", "tags"]
  filterset_class = PostFilterSet
  ordering_fields = ["published_at", "author", "title", "slug"]

  # we'll still refer to this in `get_queryset()`
  queryset = Post.objects.all()

  def get_queryset(self):

    # published only
    if self.request.user.is_anonymous:
      queryset = self.queryset.filter(published_at__lte=timezone.now())

    # allow all
    elif self.request.user.is_staff:
      queryset = self.queryset

    # filter for own or published
    else:
      queryset = self.queryset.filter(Q(published_at__lte=timezone.now()) | Q(author=self.request.user))

    # check for additional time period filtering
    time_period_name = self.kwargs.get("period_name")
    print("period:", time_period_name)

    # no further filtering
    if not time_period_name:
      return queryset

    # new (last hour)
    elif time_period_name == "new":
      return queryset.filter(published_at__gte=timezone.now() - timedelta(hours=1))

    # today
    elif time_period_name == "today":
      return queryset.filter(published_at__date=timezone.now().date())

    # week (last 7 days)
    elif time_period_name == "week":
      return queryset.filter(published_at__gte=timezone.now() - timedelta(days=7))

    # error
    else:
      raise Http404(f"Time period {time_period_name} is not valid, should be 'new', 'today' or 'week'")

  def get_serializer_class(self):
    if self.action in ("list", "create"):
      return PostSerializer
    return PostDetailSerializer

  # Override Post list, so that can cache for 2 minutes
  @method_decorator(cache_page(120))
  def list(self, *args, **kwargs):
    print("cached")
    return super(PostViewSet, self).list(*args, **kwargs)

  # Caching method decorators
  @method_decorator(cache_page(300))
  @method_decorator(vary_on_headers("Authorization", "Cookie"))
  @method_decorator(vary_on_cookie)
  @action(methods=["get"], detail=False, name="Posts by the logged in user")
  def mine(self, request):
    if request.user.is_anonymous:
      raise PermissionDenied("You must bee logged in to see which Posts are yours")
    posts = self.get_queryset().filter(author=request.user)

    # manual pagination
    page = self.paginate_queryset(posts)
    if page is not None:
      serializer = PostSerializer(page, many=True, context={"request": request})
      return self.get_paginated_response(serializer.data)

    serializer = PostSerializer(posts, many=True, context={"request": request})
    return Response(serializer.data)
