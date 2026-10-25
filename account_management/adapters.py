from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        if user.email:
            base_username = user.email.split('@')[0]
            username = base_username
            counter = 1
            
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
                
            user.username = username
            
        return user

    def get_connect_redirect_url(self, request, socialaccount):
        return reverse('account_security_info_edit')
