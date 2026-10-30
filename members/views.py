from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from feed.models import Post

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import FollowForm

from .models import Follow

def profile_view(request, user_id):
    user_profile, created = Profile.objects.get_or_create(user_id=user_id)

    user_posts = user_profile.user.feed_posts.filter(status = Post.Status.PUBLISHED).order_by('-publish')[:3]

    published_posts_count = user_profile.user.feed_posts.filter(status = Post.Status.PUBLISHED).count()

    published_comments_count = user_profile.user.comments.filter(active = True).count()

    is_me = request.user.is_authenticated and request.user == user_profile.user 

    if request.user.is_authenticated and request.user != user_profile.user: 
        
        if request.method == 'POST':
            if Follow.objects.filter(user_from = request.user.profile, user_to = user_profile):

                follow_form = FollowForm(request.POST)
                if follow_form.is_valid():
                    Follow.objects.filter(user_from = request.user.profile, user_to = user_profile).delete()
                    
                    messages.success(
                            request,
                            f"Successfully unfollowed { user_profile.user.username }"
                            )
                    return redirect("members:profile_view", user_id=user_id)
                else:
                    messages.error(
                        request,
                        f'Error unfollowing { user_profile.user.username }'
                    )
                    return redirect("members:profile_view", user_id=user_id)
                
            else:

                follow_form = FollowForm(request.POST)

                if follow_form.is_valid():
                    follow = follow_form.save(commit=False)
                    follow.user_from = request.user.profile
                    follow.user_to = user_profile

                    follow.save()

                    messages.success(
                            request,
                            f"Successfully followed { user_profile.user.username }"
                            )
                    return redirect("members:profile_view", user_id=user_id)
                else:
                    messages.error(
                        request,
                        f'Error following { user_profile.user.username }'
                    )
                    return redirect("members:profile_view", user_id=user_id)
        else:
            follow_form = FollowForm()
            if Follow.objects.filter(user_from = request.user.profile, user_to = user_profile):
                following = True
            else:
                following = False

    else:
        follow_form = None
        following = None


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
            'follow_form' : follow_form,
            'following' : following,
        }
    )

@login_required
def my_profile(request):
    return redirect("members:profile_view", user_id=request.user.id)
