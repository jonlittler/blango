from rest_framework import generics

from blog.api.serializers import PostSerializer
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from blog.models import Post


class PostList(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  # permission_classes = [AuthorModifyOrReadOnly]
  permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
