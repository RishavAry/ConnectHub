from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

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