from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    email = (models.EmailField(unique=True))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow"
            )
        ]
    def __str__(self):
        return f"{self.follower} follows {self.following}"
class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
    )
    def __str__(self):
        return f"{self.author} posted {self.content[:30]}"

class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_post_like"
            )
        ]

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"

    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

