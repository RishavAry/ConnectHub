from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Follow, Post, Like, Notification

# from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm, ProfileForm, PostForm, CommentForm
from django.db.models import Q, Count, Exists, OuterRef
from django.utils.http import url_has_allowed_host_and_scheme

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

            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()}
            ):
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

    liked_by_user = Like.objects.filter(
        user=request.user,
        post= OuterRef("pk")
    )
    posts = (Post.objects.filter(
        Q(author=request.user) |
        Q(author_id__in=following_users)
    ).select_related("author").annotate(likes_count=Count("likes"),
                                            is_liked=Exists(liked_by_user)).prefetch_related("comments")
             .order_by("-created_at")
             )

    post_data = []
    for post in posts:
        likes_count = post.likes_count

        post_data.append({
            "post": post,
            "likes_count": likes_count,
            "is_liked": post.is_liked,
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
    user = get_object_or_404(User, id=user_id)

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

    return redirect("user_profile", user_id=user_id)

@login_required
def users_list(request):
    followed_by_user = Follow.objects.filter(

        follower=request.user,
        following=OuterRef("pk")
    )
    users = User.objects.exclude(
        id=request.user.id
    ).annotate(
        is_following=Exists(followed_by_user)
    )

    user_data = []

    for user in users:
        user_data.append({
            "user": user,
            "is_following": user.is_following,
        })

    return render(
        request,
        "accounts/users.html",
        {"users": user_data,}
    )

@login_required
def unfollow_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    Follow.objects.filter(
        follower=request.user,
        following=user
    ).delete()

    return redirect("user_profile", user_id=user_id)

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
    post = get_object_or_404(Post, id=post_id)
    next_url = request.GET.get("next")
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
        if request.user != post.author:
            Notification.objects.create(
                sender=request.user,
                recipient=post.author,
                notification_type="like",
                post=post,
            )
    if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()}
    ):
        return redirect(next_url)

    return redirect("home")


@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            if request.user != post.author:
                Notification.objects.create(
                    sender=request.user,
                    recipient=post.author,
                    notification_type="comment",
                    post=post,
                    comment=comment

                )
    return redirect("post_detail", post_id=post_id)


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
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)

    notification.is_read = True
    notification.save()
    return redirect("notifications")

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    liked_by_user = Like.objects.filter(
        user=request.user,
        post=OuterRef("pk")
    )
    posts = user.posts.all().annotate(
        is_liked= Exists(liked_by_user),
    )

    followers_count = user.followers.count()
    following_count = user.following.count()
    is_following = Follow.objects.filter(
        follower=request.user,
        following=user
    ).exists()
    return render(
        request,
        "accounts/user_profile.html",
        {
            "user": user,
            "posts": posts,
            "followers_count": followers_count,
            "following_count": following_count,
            "is_following": is_following
        }
    )




def search_users(request):
    query = request.GET.get("q")

    if query:
        users = User.objects.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
        ).exclude(id=request.user.id)
    else:
        users = User.objects.none()

    return render(
        request,
        "accounts/search.html",
        {"users": users}
    )

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_liked = post.likes.filter(
        user=request.user
    ).exists()
    comment_form = CommentForm()

    return render(
        request,
        "accounts/post_detail.html",
        {"post": post, "is_liked": is_liked, "comment_form": comment_form}
    )


