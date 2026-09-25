from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Post, Like, Notification,Comment
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from .permissions import IsPostAuthor
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