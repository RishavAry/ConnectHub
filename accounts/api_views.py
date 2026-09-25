from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Post, Like, Notification, Comment, Follow, Profile
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from .permissions import IsPostAuthor
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from rest_framework import status
from .forms import RegistrationForm, ProfileForm
from .models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import CsrfViewMiddleware, get_token
from django.db.models import Exists, OuterRef
from .views import (
    follow_user_record,
    unfollow_user_record,
    search_user_queryset,
    mark_notification_as_read,
)
@api_view(['GET'])
def hello_api(request):
    return Response({"message": "connecthub"})

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def post_list_view(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
@api_view(['GET','PUT','PATCH', 'DELETE'])
@permission_classes((IsAuthenticated,))
def post_detail_api(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # serializer = PostSerializer(post)
    if request.method in ['PUT', 'PATCH', 'DELETE']:
        if request.user != post.author:
            raise PermissionDenied("You are not authorized to edit this post")
    if request.method == 'DELETE':
        post.delete()
        return Response({"message": "Post deleted successfully"})
    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    if request.method == 'PATCH':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    # return Response(serializer.data)


class PostDetailApi(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]
    def get_object(self, post_id):
        return get_object_or_404(Post, id=post_id)
    def get(self, request, post_id):
        post = self.get_object(post_id)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_id):
        post = self.get_object(post_id)

        self.check_object_permissions(request, post)

        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def patch(self, request, post_id):
        post = self.get_object(post_id)

        self.check_object_permissions(request, post)

        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, post_id):
        post = self.get_object(post_id)

        self.check_object_permissions(request, post)

        post.delete()

        return Response({"message": "Post deleted successfully"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post_api(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()
    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )
        liked = True

        if request.user != post.author:
            Notification.objects.create(
                sender=request.user,
                recipient=post.author,
                notification_type="like",
                post=post,
            )
    return Response({
                "liked":liked,
                "likes_count": post.likes.count(),
    })

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def create_comment_api(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "GET":
        comments = Comment.objects.filter(
            post=post
        ).order_by("created_at")

        serializer = CommentSerializer(
            comments,
            many=True
        )

        return Response(serializer.data)

    content = request.data.get("content")

    if not content:
        return Response(
            {"error": "Comment cannot be empty"},
            status=400
        )

    comment = Comment.objects.create(
        post=post,
        user=request.user,
        content=content
    )

    if request.user != post.author:
        Notification.objects.create(
            sender=request.user,
            recipient=post.author,
            notification_type="comment",
            post=post,
            comment=comment,
        )

    serializer = CommentSerializer(comment)
    return Response(serializer.data)

@api_view(["POST"])
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Invalid username or password"},
            status=400
        )

    login(request, user)

    return Response({
        "message": "Login successful",
        "username": user.username,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user_api(request):
    return Response({
        "id": request.user.id,
        "username": request.user.username,
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_api(request):
    logout(request)

    return Response({
        "message": "Logout successful"
    })


@api_view(["POST"])
def registration_api(request):
    # DRF exempts API views from Django's outer CSRF middleware. Registration
    # is public, so SessionAuthentication would otherwise skip CSRF validation.
    csrf_middleware = CsrfViewMiddleware(lambda _request: None)
    django_request = request._request
    csrf_middleware.process_request(django_request)
    csrf_failure = csrf_middleware.process_view(
        django_request,
        lambda _request: None,
        (),
        {},
    )
    if csrf_failure:
        return Response(
            {"detail": "CSRF verification failed. Please refresh and try again."},
            status=status.HTTP_403_FORBIDDEN,
        )

    form = RegistrationForm(data=request.data)
    if not form.is_valid():
        errors = {
            field: [error["message"] for error in field_errors]
            for field, field_errors in form.errors.get_json_data().items()
        }
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    data = form.cleaned_data
    user = User.objects.create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
    )
    return Response(
        {"message": "Registration successful. Please sign in.", "username": user.username},
        status=status.HTTP_201_CREATED,
    )


@ensure_csrf_cookie
@api_view(["GET"])
def csrf_token_api(request):
    """Set the CSRF cookie for the session based React client."""
    return Response({"csrfToken": get_token(request)})


def _profile_data(user, viewer):
    profile, _ = Profile.objects.get_or_create(user=user)
    return {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": profile.bio,
        "location": profile.location,
        "posts_count": user.posts.count(),
        "followers_count": user.followers.count(),
        "following_count": user.following.count(),
        "is_following": Follow.objects.filter(follower=viewer, following=user).exists(),
    }


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def profile_api(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "PATCH":
        form = ProfileForm(data=request.data, instance=profile)
        if not form.is_valid():
            errors = {
                field: [item["message"] for item in field_errors]
                for field, field_errors in form.errors.get_json_data().items()
            }
            return Response({"errors": errors}, status=400)
        form.save()
    return Response(_profile_data(request.user, request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile_api(request, user_id):
    user = get_object_or_404(User, id=user_id)
    data = _profile_data(user, request.user)
    liked_by_user = Like.objects.filter(user=request.user, post=OuterRef("pk"))
    posts = user.posts.annotate(is_liked=Exists(liked_by_user)).order_by("-created_at")
    data["posts"] = PostSerializer(posts, many=True).data
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_search_api(request):
    query = request.query_params.get("q", "").strip()
    if not query:
        return Response([])
    followed_by_user = Follow.objects.filter(follower=request.user, following=OuterRef("pk"))
    users = search_user_queryset(query, request.user).annotate(is_following=Exists(followed_by_user)).order_by("username")
    return Response([{
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_following": user.is_following,
    } for user in users])


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def follow_api(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        return Response({"detail": "You cannot follow yourself."}, status=400)
    if request.method == "POST":
        follow_user_record(request.user, user)
        following = True
    else:
        unfollow_user_record(request.user, user)
        following = False
    return Response({
        "following": following,
        "followers_count": user.followers.count(),
        "following_count": request.user.following.count(),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notifications_api(request):
    notifications = Notification.objects.filter(recipient=request.user).select_related("sender", "post").order_by("-created_at")
    return Response([{
        "id": notification.id,
        "sender": notification.sender.username,
        "type": notification.notification_type,
        "created_at": notification.created_at,
        "is_read": notification.is_read,
        "post_id": notification.post_id,
    } for notification in notifications])


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_notification_read_api(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    mark_notification_as_read(notification)
    return Response({"id": notification.id, "is_read": notification.is_read})
