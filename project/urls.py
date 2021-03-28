from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from health_check import urls as health_urls

from project.apps.video_archive import urls as video_archive_urls
from project.apps.video_archive.views import VideosListView

admin.autodiscover()

urlpatterns = [
    # Apps:
    path('video-archive/', include(video_archive_urls, namespace='video_archive')),

    # Health checks:
    path('health/', include(health_urls)),  # noqa: DJ05

    # django-admin:
    path('admin/', admin.site.urls),

    # It is a good practice to have explicit index view:
    path('', VideosListView.as_view(), name='index'),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path('__debug__/', include(debug_toolbar.urls)),  # noqa: DJ05
    ] + urlpatterns + static(  # type: ignore
        # Serving media files in development only:
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
