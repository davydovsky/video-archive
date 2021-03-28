import os
import subprocess
import tempfile

from django.conf import settings
from video_encoding import exceptions
from video_encoding.backends.ffmpeg import FFmpegBackend


class VideoEncodingBackend(FFmpegBackend):
    """Override default video encoding backend."""

    def get_thumbnail(self, video_path: str, at_time: float = 0.5) -> str:
        """Override base class function to add thumbnail scaling."""
        filename = os.path.basename(video_path)
        filename, __ = os.path.splitext(filename)
        _, image_path = tempfile.mkstemp(suffix=f'_{filename}.jpg')

        video_duration = self.get_media_info(video_path)['duration']
        if at_time > video_duration:
            raise exceptions.InvalidTimeError()
        thumbnail_time = at_time

        cmd = [self.ffmpeg_path, '-i', video_path, '-vframes', '1', '-vf', f'scale={settings.VIDEO_SCALE}']
        cmd.extend(['-ss', str(thumbnail_time), '-y', image_path])

        subprocess.check_call(cmd)

        if not os.path.getsize(image_path):
            # we somehow failed to generate thumbnail
            os.unlink(image_path)
            raise exceptions.InvalidTimeError()

        return image_path
