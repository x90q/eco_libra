from django.shortcuts import render, get_object_or_404
from account.models import Profile

def profile_view(request, user_id):
    user_profile = get_object_or_404(
        Profile.objects.select_related('user'),
        user__id=user_id,
    )

    is_me = request.user.is_authenticated and request.user == user_profile.user

    return render(
        request,
        'members/profile_view.html',
        {
            'user_id' : user_id,
            'user_profile' : user_profile,
            'is_me' : is_me
        }
    )
