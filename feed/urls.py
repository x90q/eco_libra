from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path(
        '<slug:category>/post/<slug:post>/', 
        views.post_detail, 
        name = 'post_detail'
        ),
    path(
        'post/<int:post_id>/share/',
        views.post_share,
        name = 'post_share',
    ),
    path(
            'post/<int:post_id>/comment/',
        views.post_comment,
        name = 'post_comment'
    ),

    path(
        '',
        views.home,
        name = 'home'
    ),
    path(
        'latest/',
        views.post_list,
        name = 'post_list_all'
    ),
    path(
        'category/<slug:category_slug>/',
        views.post_list,
        name = 'post_list_by_category'
        ),
    path(
        'tag/<slug:tag_slug>/',
        views.post_list,
        name = 'post_list_by_tag'
    ),
    path(
        'post/create/',
        views.post_create,
        name = 'post_create'
    )
]