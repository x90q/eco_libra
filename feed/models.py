from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.functions import Now
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status = Post.Status.PUBLISHED)
        )

class Category(models.Model):
    name = models.CharField(max_length=15)
    slug = models.CharField(max_length=20)

    color = models.TextField(max_length=7, default = "#ffffff")

    class Meta:
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    
class Post(models.Model):

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feed_posts'
    )

    category = models.ForeignKey(
            Category,
            on_delete = models.CASCADE,
            related_name = "posts"
        )
    
    body = models.TextField()

    publish = models.DateTimeField(db_default = Now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=2,
        choices = Status.choices,
        default = Status.DRAFT
    )

    views = models.IntegerField(default = 0)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields = ['-publish']),
        ]
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'feed:post_detail',
            args = [
                self.category.slug,
                self.slug
            ]
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status != Post.Status.PUBLISHED:
            self.comments.filter(active=True).update(active=False)
        else:
            self.comments.filter(active=False).update(active=True)

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name = 'comments'
    )

    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='comments'
        )
    body = models.TextField(max_length = 500)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default = True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields = ['created']),
        ]

    def __str__(self):
        return f"Comment by { self.user.username } on { self.post }"

    def get_absolute_url(self):
            return reverse(
                'feed:post_detail',
                args = [
                    self.post.category.slug,
                    self.post.slug
                ]
            )
    