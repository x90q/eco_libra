from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path(
        '',
        views.search_results,
        name = 'search_results'
    ),
    path(
        'user_posts/<int:user_id>',
        views.posts_from_user,
        name = 'posts_from_user'
    ),
    path(
        'user_comments/<int:user_id>',
        views.comments_from_user,
        name = 'comments_from_user'
    )
]