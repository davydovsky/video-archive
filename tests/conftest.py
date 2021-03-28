import base64
import io

import pytest
from django.core.files.uploadedfile import UploadedFile
from hypothesis.extra.django import register_field_strategy
from hypothesis.strategies import just
from video_encoding.fields import VideoField

from project.apps.video_archive.encoding_backends import VideoEncodingBackend
from project.apps.video_archive.models import Video


video_file_base64 = 'AAAAIGZ0eXBpc29tAAACAGlzb21pc28yYXZjMW1wNDEAAAAIZnJlZQAABRptZGF0AAACrgYF//' \
                    '+q3EXpvebZSLeWLNgg2SPu73gyNjQgLSBjb3JlIDE1MiByMjg1NCBlOWE1OTAzIC0gSC4yNjQvT' \
                    'VBFRy00IEFWQyBjb2RlYyAtIENvcHlsZWZ0IDIwMDMtMjAxNyAtIGh0dHA6Ly93d3cudmlkZW9s' \
                    'YW4ub3JnL3gyNjQuaHRtbCAtIG9wdGlvbnM6IGNhYmFjPTEgcmVmPTMgZGVibG9jaz0xOjA6MCBh' \
                    'bmFseXNlPTB4MzoweDExMyBtZT1oZXggc3VibWU9NyBwc3k9MSBwc3lfcmQ9MS4wMDowLjAwIG1p' \
                    'eGVkX3JlZj0xIG1lX3JhbmdlPTE2IGNocm9tYV9tZT0xIHRyZWxsaXM9MSA4eDhkY3Q9MSBjcW09' \
                    'MCBkZWFkem9uZT0yMSwxMSBmYXN0X3Bza2lwPTEgY2hyb21hX3FwX29mZnNldD0tMiB0aHJlYWRzP' \
                    'TEgbG9va2FoZWFkX3RocmVhZHM9MSBzbGljZWRfdGhyZWFkcz0wIG5yPTAgZGVjaW1hdGU9MSBpbnR' \
                    'lcmxhY2VkPTAgYmx1cmF5X2NvbXBhdD0wIGNvbnN0cmFpbmVkX2ludHJhPTAgYmZyYW1lcz0zIGJfc' \
                    'HlyYW1pZD0yIGJfYWRhcHQ9MSBiX2JpYXM9MCBkaXJlY3Q9MSB3ZWlnaHRiPTEgb3Blbl9nb3A9MCB' \
                    '3ZWlnaHRwPTIga2V5aW50PTI1MCBrZXlpbnRfbWluPTI1IHNjZW5lY3V0PTQwIGludHJhX3JlZnJl' \
                    'c2g9MCByY19sb29rYWhlYWQ9NDAgcmM9Y3JmIG1idHJlZT0xIGNyZj0yMy4wIHFjb21wPTAuNjAgc' \
                    'XBtaW49MCBxcG1heD02OSBxcHN0ZXA9NCBpcF9yYXRpbz0xLjQwIGFxPTE6MS4wMACAAAAATGWIhAC' \
                    'f2dNrpu0+0W5Pi8zqRgiToX6NJuz2vc+yG/h/sFPFaHBU05qUOJHL2BxysQI8vKcfsGk+N5XvRqzb/' \
                    'paq6M74k+6MAR6yY/0AAAAIQZokbEn/nIAAAAAIQZ5CeIQ/6YEAAAAIAZ5hdELf7YAAAAAIAZ5jakL' \
                    'f7YEAAAAUQZplSahBaJlMCT+yvESW1o+/Al8AAAANQZqISeEKUmUwJv+mgQAAAApBnqZFNEwp/+yBAA' \
                    'AACAGex2pC3+2AAAAADUGayUmoQWiZTAm/poAAAAANQZrqSeEKUmUwJv+mgQAAABFBmwtJ4Q6JlMCb/' \
                    '/dus8NTXwAAAA9BmyxJ4Q8mUwJv8GXSotoAAAAQQZtNSeEPJlMCb7yc7UUD7wAAAA5Bm25J4Q8mUwJvvJ' \
                    'nKWQAAABFBm49J4Q8mUwJvvJjTsrDYyQAAABJBm7BJ4Q8mUwIj/7OD4thRzUQAAAARQZvRSeEPJlMCI/+z' \
                    'iHbfi/AAAAASQZvySeEPJlMCI/+zhZGHxtHlAAAAEkGaE0nhDyZTAiP/s4Yl1lMZQAAAABNBmjRJ4Q8mUw' \
                    'Ij/7ONuGizdf7AAAAADUGaVUnhDyZTAiv/s4EAAAATQZp2SeEPJlMCK//c7QVPCWARwAAAABNBmphJ4Q8m' \
                    'UwURPGffDIPN1MpZAAAACAGet2pC3+2BAAAADUGauUnhDyZTAjv/voAAAAASQZraSeEPJlMCO//GarkCeW' \
                    '6PAAAADUGa+0nhDyZTAhD/wYAAAAAQQZscSeEPJlMCEv/N1e/9QQAAAA9Bmz1J4Q8mUwIW/9ObfX8AAAP+' \
                    'bW9vdgAAAGxtdmhkAAAAAAAAAAAAAAAAAAAD6AAAA+gAAQAAAQAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAA' \
                    'AAAAABAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAyh0cmFrAAAA' \
                    'XHRraGQAAAADAAAAAAAAAAAAAAABAAAAAAAAA+gAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAA' \
                    'BAAAAAAAAAAAAAAAAAABAAAAAAAoAAAAKAAAAAAAkZWR0cwAAABxlbHN0AAAAAAAAAAEAAAPoAAAEAAABAA' \
                    'AAAAKgbWRpYQAAACBtZGhkAAAAAAAAAAAAAAAAAAA8AAAAPABVxAAAAAAALWhkbHIAAAAAAAAAAHZpZGUAAA' \
                    'AAAAAAAAAAAABWaWRlb0hhbmRsZXIAAAACS21pbmYAAAAUdm1oZAAAAAEAAAAAAAAAAAAAACRkaW5mAAAAHG' \
                    'RyZWYAAAAAAAAAAQAAAAx1cmwgAAAAAQAAAgtzdGJsAAAAq3N0c2QAAAAAAAAAAQAAAJthdmMxAAAAAAAAAAE' \
                    'AAAAAAAAAAAAAAAAAAAAAAAoACgBIAAAASAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                    'AAGP//AAAANWF2Y0MBZAAK/+EAGGdkAAqs2V+STARAAAADAEAAAA8DxIllgAEABmjr48siwP34+AAAAAAQcGF' \
                    'zcAAAAAEAAAABAAAAGHN0dHMAAAAAAAAAAQAAAB4AAAIAAAAAFHN0c3MAAAAAAAAAAQAAAAEAAABwY3R0cwAAA' \
                    'AAAAAAMAAAAAQAABAAAAAABAAAKAAAAAAEAAAQAAAAAAQAAAAAAAAABAAACAAAAAAEAAAQAAAAAAQAACAAAAAACA' \
                    'AACAAAAAA4AAAQAAAAAAQAABgAAAAABAAACAAAAAAUAAAQAAAAAHHN0c2MAAAAAAAAAAQAAAAEAAAAeAAAAAQAA' \
                    'AIxzdHN6AAAAAAAAAAAAAAAeAAADAgAAAAwAAAAMAAAADAAAAAwAAAAYAAAAEQAAAA4AAAAMAAAAEQAAABEAAAA' \
                    'VAAAAEwAAABQAAAASAAAAFQAAABYAAAAVAAAAFgAAABYAAAAXAAAAEQAAABcAAAAXAAAADAAAABEAAAAWAAAAEQ' \
                    'AAABQAAAATAAAAFHN0Y28AAAAAAAAAAQAAADAAAABidWR0YQAAAFptZXRhAAAAAAAAACFoZGxyAAAAAAAAAABtZG' \
                    'lyYXBwbAAAAAAAAAAAAAAAAC1pbHN0AAAAJal0b28AAAAdZGF0YQAAAAEAAAAATGF2ZjU4LjQ1LjEwMA=='


@pytest.fixture(autouse=True)
def _media_root(settings, tmpdir_factory) -> None:
    """Forces django to save media files into temp folder."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)


@pytest.fixture(autouse=True)
def _debug(settings) -> None:
    """Sets proper DEBUG and TEMPLATE debug mode for coverage."""
    settings.DEBUG = False
    for template in settings.TEMPLATES:
        template['OPTIONS']['debug'] = True


@pytest.fixture(autouse=True)
def _task_always_eager(settings) -> None:
    """Enable sync tasks execution."""
    settings.CELERY_DEFAULT_TASK_ALWAYS_EAGER = True


@pytest.fixture()
def main_heading() -> str:
    """Get index page heading page."""
    return 'Video Archive'


def video_file_example() -> UploadedFile:
    """Get example video file."""
    file = io.BytesIO(base64.b64decode(video_file_base64))
    return UploadedFile(file=file, name='video file example',
                        content_type='video/mp4', size=file.getbuffer().nbytes)


register_field_strategy(VideoField, just(video_file_example()))


@pytest.fixture
def video_instance() -> Video:
    return Video.objects.create(file=video_file_example())


@pytest.fixture
def video_encoding_backend() -> VideoEncodingBackend:
    return VideoEncodingBackend()
