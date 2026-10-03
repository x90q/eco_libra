from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d',
        blank = True
    )
    date_of_birth = models.DateField(blank = True, null= True)
    bio = models.TextField(max_length=100, blank = True, default = '')

    def __str__(self):
        return f'Profile of { self.user.username }'
