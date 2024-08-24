from django.urls import path
from blog.api_views import post_list, post_detail
from rest_framework.urlpatterns import format_suffix_patterns

# Not Used Anymore - see api.urls.py

urlpatterns = [
  path("posts/", post_list, name="api_post_list"),
  path("posts/<int:pk>", post_detail, name="api_post_detail"),  # remove trailing /
]

urlpatterns = format_suffix_patterns(urlpatterns)
