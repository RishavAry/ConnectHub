from django.urls import path
from .api_views import hello_api, post_list_view, post_detail_api

urlpatterns = [
    path("hello/", hello_api, name="hello_api"),
    path("posts/", post_list_view, name="posts_list_view"),
    path("posts/<int:post_id>/", post_detail_api, name="post_detail_api"),
]