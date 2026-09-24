from django.urls import path
from . import views

app_name = 'blog'

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
        'category/<slug:category>/',
        views.category_list,
        name = 'category_list'
        )
]