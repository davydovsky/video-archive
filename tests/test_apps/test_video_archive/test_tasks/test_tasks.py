from hypothesis import given, settings
from hypothesis.extra import django
from hypothesis.strategies import just

from project.apps.video_archive.models import Video
from project.apps.video_archive.tasks import convert_all_videos, create_preview, handle_file_via_url


class TestTasks(django.TestCase):
    """This async tasks logic."""

    @settings(deadline=1000)
    @given(django.from_model(Video, width=just(None), height=just(None),
                             duration=just(None), preview=just('')))
    def test_video_converted(self, video_instance: Video) -> None:
        """Tests that video was converted in all formats."""
        convert_all_videos('video_archive', 'Video', video_instance.pk)
        assert video_instance.format_set.complete().all().count() == 2

    @given(django.from_model(Video, width=just(None), height=just(None),
                             duration=just(None), preview=just('')))
    def test_preview_creation(self, video_instance: Video) -> None:
        """Tests that preview is created."""
        create_preview(video_instance.pk)
        assert video_instance.preview is not ''

