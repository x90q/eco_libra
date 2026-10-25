from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from feed.models import Post

from django.contrib.auth.decorators import login_required

from django.contrib import messages

def profile_view(request, user_id):
    user_profile, created = Profile.objects.get_or_create(user_id=user_id)

    user_posts = user_profile.user.feed_posts.filter(status = Post.Status.PUBLISHED).order_by('-publish')[:3]

    published_posts_count = user_profile.user.feed_posts.filter(status = Post.Status.PUBLISHED).count()

    published_comments_count = user_profile.user.comments.filter(active = True).count()

    is_me = request.user.is_authenticated and request.user == user_profile.user 

    return render(
        request,
        'members/profile_view.html',
        {
            'user_id' : user_id,
            'user_profile' : user_profile,
            'is_me' : is_me,
            'user_posts' : user_posts,
            'published_posts_count' : published_posts_count,
            'published_comments_count' : published_comments_count,
        }
    )

@login_required
def my_profile(request):
    return redirect("members:profile_view", user_id=request.user.id)
