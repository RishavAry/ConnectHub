from django.urls import path
from .api_views import hello_api, post_list_view, PostDetailApi, like_post_api, create_comment_api, login_api, current_user_api,logout_api

urlpatterns = [
    path("hello/", hello_api, name="hello_api"),
    path("posts/", post_list_view, name="posts_list_view"),
    path(
        "posts/<int:post_id>/",
        PostDetailApi.as_view(),
        name="post_detail_api"
    ),
    path("posts/<int:post_id>/like/", like_post_api, name="like_post_api"),
    path(
    "posts/<int:post_id>/comments/",
    create_comment_api,
    name="create_comment_api"
    ),
    path(
    "login/",
    login_api,
    name="login_api"
    ),
    path(
    "me/",
    current_user_api,
    name="current_user_api",
    ),
    path(
        "logout/",
        logout_api,
        name="logout_api",
    ),
    ]