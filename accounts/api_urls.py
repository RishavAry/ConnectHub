from django.urls import path
from .api_views import hello_api, post_list_view, PostDetailApi

urlpatterns = [
    path("hello/", hello_api, name="hello_api"),
    path("posts/", post_list_view, name="posts_list_view"),
    path(
        "posts/<int:post_id>/",
        PostDetailApi.as_view(),
        name="post_detail_api"
    ),]