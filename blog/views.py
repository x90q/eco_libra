from django.shortcuts import render, get_object_or_404

from .models import Post

def post_list(request):
    posts = Post.published.all()
    return render(
        request,
        'blog/post/post_list.html',
        {'posts': posts}
    )

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        status = Post.Status.PUBLISHED,
        slug = post_slug,
        publish__year = year,
        publish__month = month,
        publish__day = day
    )
    return render(
        request,
        'blog/post/post_detail.html',
        {'post': post}
    )
# Create your views here.
