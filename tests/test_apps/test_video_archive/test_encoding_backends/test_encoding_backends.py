import os

import pytest
from video_encoding.exceptions import InvalidTimeError

from project.apps.video_archive.encoding_backends import VideoEncodingBackend
from project.apps.video_archive.models import Video


class TestVideoEncodingBackend(object):
    """Check custom encoding backend."""

    @pytest.mark.django_db()
    def test_image_preview_creation_success(self, video_encoding_backend: VideoEncodingBackend,
                                            video_instance: Video) -> None:
        """Tests that thumbnail was crated successfully."""
        assert os.path.getsize(video_encoding_backend.get_thumbnail(video_instance.file.path)) > 0

    @pytest.mark.django_db()
    def test_image_preview_creation_wrong_duration(self, video_encoding_backend: VideoEncodingBackend,
                                                   video_instance: Video) -> None:
        """Tests that the video is shorter than given time code."""
        with pytest.raises(InvalidTimeError):
            video_encoding_backend.get_thumbnail(video_instance.file.path, at_time=10)
