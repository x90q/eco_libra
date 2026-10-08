from django.contrib.auth.models import User

from account.models import Profile

class EmailAuthBackend:

    def authenticate(self, request, username = None, password = None):
        try:
            user = User.objects.get(email = username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
    
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user if user.is_active else None
        except User.DoesNotExist:
            return None

def create_profile(backend, user, *args, **kwargs):
    # create profile for user created via oauth
    Profile.objects.get_or_create(user=user)