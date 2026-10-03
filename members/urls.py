from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path(
        '<int:user_id>/',
        views.profile_view,
        name = 'profile_view',
    )
]