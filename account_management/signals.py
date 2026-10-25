from allauth.account.signals import email_confirmed
from django.dispatch import receiver

from ..members.models import Profile

@receiver(email_confirmed)
def create_profile_after_email_confirmation(request, email_address, **kwargs):
    Profile.objects.get_or_create(user=email_address.user)