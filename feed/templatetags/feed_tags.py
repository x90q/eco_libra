from django import template
from ..models import Post, Category
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('feed/post/latest_posts.html')
def show_latest_posts(count = 5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {
        'latest_posts' : latest_posts
    }

@register.simple_tag
def get_most_commented_posts(count = 5):
    return Post.published.annotate(
        total_comments = Count('comments')
    ).order_by('-total_comments')[:count]

@register.simple_tag
def get_most_popular_categories(count = 5):
    return Category.objects.annotate(
        total_posts = Count('posts')
    ).order_by('-total_posts')[:count]
