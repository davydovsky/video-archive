from django.urls import path

from project.apps.video_archive import views

app_name = 'video_archive'

urlpatterns = [
    path('', views.VideosListView.as_view(), name='video-feed'),
]
