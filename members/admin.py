from django.contrib import admin
from .models import Profile, Follow

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'date_of_birth']
    raw_id_fields = ['user']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']
