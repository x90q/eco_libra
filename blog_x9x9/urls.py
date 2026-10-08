from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from feed.sitemaps import PostSitemap

from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    'posts' : PostSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed/', include('feed.urls', namespace='feed')),
    path('account/', include('account.urls', namespace = 'account')),
    path(
        'social-auth/',
        include(
            'social_django.urls',
            namespace = 'social'
        ),
        ),
    path('search/', include('search.urls', namespace = 'search')),
    path('members/', include('members.urls', namespace = 'members')),
    path(
        'sitemap.xml',
        sitemap,
        { 'sitemaps' : sitemaps },
        name = 'django.contrib.sitemaps.views.sitemap'
    )
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )
