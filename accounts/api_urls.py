from django.urls import path
from .api_views import (
    hello_api, post_list_view, PostDetailApi, like_post_api,
    create_comment_api, login_api, registration_api, current_user_api,
    logout_api, csrf_token_api, profile_api, user_profile_api,
    user_search_api, follow_api, notifications_api,
    mark_notification_read_api,
)

urlpatterns = [
    path("hello/", hello_api, name="hello_api"),
    path("csrf/", csrf_token_api, name="csrf_token_api"),
    path("register/", registration_api, name="registration_api"),
    path("profile/", profile_api, name="profile_api"),
    path("users/search/", user_search_api, name="user_search_api"),
    path("users/<int:user_id>/profile/", user_profile_api, name="user_profile_api"),
    path("users/<int:user_id>/follow/", follow_api, name="follow_api"),
    path("notifications/", notifications_api, name="notifications_api"),
    path("notifications/<int:notification_id>/read/", mark_notification_read_api, name="mark_notification_read_api"),
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
