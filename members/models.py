from django.db import models
from django.conf import settings

class Follow(models.Model):
    user_from = models.ForeignKey(
        'Profile',
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )

    user_to = models.ForeignKey(
        'Profile',
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )

    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        # no same followings in db
        constraints = [
            models.UniqueConstraint(fields = ['user_from', 'user_to'], name = 'unique_followers')
        ]

        indexes = [
            models.Index(fields = ['user_from', 'user_to'])
        ]

        ordering = ['-created',]

    def __str__(self):
        return f"{self.user_from.user.username} follows {self.user_to.user.username}"

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

    following = models.ManyToManyField(
        'self',
        through=Follow,
        related_name='followers',
        symmetrical=False,
        through_fields=('user_from', 'user_to')
    )

    def __str__(self):
        return f'Profile of { self.user.username }'

