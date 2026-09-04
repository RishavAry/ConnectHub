from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .models import User, Follow, Post, Like, Notification
from .forms import RegistrationForm, LoginForm
# from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, ProfileForm, PostForm, CommentForm
from django.db.models import Q

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
            )
            return redirect('login')

        else:
            form = RegistrationForm()

        return render(request, 'accounts/register.html', {'form': form})


    return render(request, 'accounts/register.html')

def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["user"]

            login(request, user)

            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("home")

    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )

@login_required
def home(request):
    following_users = request.user.following.values_list(
        "following",
        flat=True
    )


    posts = Post.objects.filter(
        Q(author=request.user) |
        Q(author_id__in=following_users)
    ).order_by("-created_at")

    post_data = []
    for post in posts:
        likes_count = post.likes.count()
        is_liked = Like.objects.filter(
            user=request.user,
            post=post
        ).exists()
        post_data.append({
            "post": post,
            "likes_count": likes_count,
            "is_liked": is_liked,
            "comment_form": CommentForm(),
        })

    return render(
        request,
        "accounts/home.html",
        {"posts": post_data,
         }
    )


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    context = {
        'form': form,
        'posts_count': request.user.posts.count(),
        'followers_count': request.user.followers.count(),
        'following_count': request.user.following.count(),
    }

    return render(request, "accounts/profile.html", context)

@login_required
def follow_user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.user == user:
        return redirect("users")

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user
    )

    if created:
        Notification.objects.create(
            sender=request.user,
            recipient=user,
            notification_type="follow",
        )

    return redirect("users")

@login_required
def users_list(request):
    users = User.objects.exclude(id=request.user.id)
    user_data = []

    for user in users:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()

        user_data.append({
            "user": user,
            "is_following": is_following
        })

    return render(
        request,
        "accounts/users.html",
        {"users": user_data}
    )

@login_required
def unfollow_user(request, user_id):
    user = User.objects.get(id=user_id)

    Follow.objects.filter(
        follower=request.user,
        following=user
    ).delete()

    return redirect("users")

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("profile")

    else:
        form = PostForm()

    return render(
        request,
        "accounts/create_post.html",
        {"form": form}
    )

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()
    if like:
        like.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )

        Notification.objects.create(
            sender=request.user,
            recipient=post.author,
            notification_type="like",
            post=post,
        )
    return redirect("home")

@login_required
def comment_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            Notification.objects.create(
                sender=request.user,
                recipient=post.author,
                notification_type="comment",
                post=post,
                comment=comment

            )
    return redirect("home")


@login_required
def following(request):
    user = request.user

    following_users = User.objects.filter(
        followers__follower=user
    )

    return render(
        request,
        "accounts/following.html",
        {"users": following_users}
    )

@login_required
def followers(request):
    user = request.user
    follower_users = User.objects.filter(
        following__following=user
    )
    return render(
        request,
        "accounts/follower.html",
        {"users": follower_users}
    )

@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(
        recipient=user
    ).order_by("-created_at")
    return render(
        request,
        "accounts/notifications.html",
        {"notifications": notifications}
    )

@login_required
def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect("notifications")