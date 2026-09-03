from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
path("login/", views.login_view, name="login"),
    path("", views.home, name="home"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),

    path("follow/<int:user_id>/", views.follow_user, name="follow"),
    path("users/", views.users_list, name="users"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow"),
    path("create_post/", views.create_post, name="create_post"),
]
