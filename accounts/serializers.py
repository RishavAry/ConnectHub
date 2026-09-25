from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username' , read_only=True)
    likes_count = serializers.IntegerField(
        source="likes.count",
        read_only=True
    )
    class Meta:
        model = Post
        fields = ('id',
                  'author',
                  'content',
                  'created_at',
                  'image',
                  'likes_count')



class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "username",
            "content",
            "created_at",
        )
