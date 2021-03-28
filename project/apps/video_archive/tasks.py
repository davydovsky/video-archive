import os
import tempfile
import types
from urllib import request

from celery import shared_task
from django.conf import settings
from django.core.files import File
from video_encoding import tasks
from video_encoding.backends import get_backend

DEFAULT_KWARGS = types.MappingProxyType({
    'soft_time_limit': settings.SOFT_TIME_LIMIT,
    'time_limit': settings.SOFT_TIME_LIMIT + 100,
})


@shared_task(**DEFAULT_KWARGS)
def create_preview(video_pk: int) -> None:
    """
    Create preview image for the given video.

    :param video_pk: video primary key
    :return: None
    """
    from project.apps.video_archive.models import Video

    video = Video.objects.get(pk=video_pk)
    if not video.file:
        # no video file attached
        return
    if video.preview:
        # preview has already been generated
        return

    preview_path = get_backend().get_thumbnail(video.file.path)
    filename = os.path.basename(preview_path)

    with open(preview_path, 'rb') as file_handler:
        django_file = File(file_handler)
        video.preview.save(filename, django_file)
    video.save()


@shared_task(**DEFAULT_KWARGS)
def convert_all_videos(app_label: str, model_name: str, video_pk: int) -> None:
    """
    Wrapper task for third party library convert function.

    :param app_label: video app label
    :param model_name: video model name
    :param video_pk: video primary key
    :return: None
    """
    tasks.convert_all_videos(app_label, model_name, video_pk)


@shared_task(**DEFAULT_KWARGS)
def handle_file_via_url(url: str):
    """
    Handle file upload via url link.

    :param url:
    :return:
    """
    from project.apps.video_archive.models import Video

    # https://www.w3schools.com/html/mov_bbb.mp4
    _, file_path = tempfile.mkstemp(dir=settings.MEDIA_ROOT)
    try:
        request.urlretrieve(url, file_path)
        with open(file_path, 'rb') as file_handler:
            return Video.objects.create(file=File(file_handler))
    finally:
        os.unlink(file_path)
