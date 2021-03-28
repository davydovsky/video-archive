from hypothesis import given, settings
from hypothesis.extra import django
from hypothesis.strategies import just

from project.apps.video_archive.models import Video


class TestVideo(django.TestCase):
    """This is a property-based test that ensures model correctness."""

    @settings(deadline=1000)
    @given(django.from_model(Video, width=just(None), height=just(None),
                             duration=just(None), preview=just('')))
    def test_model_properties(self, instance: Video) -> None:
        """Tests that instance can be saved and has correct representation."""
        instance.save()

        assert instance.id > 0
        assert instance.__str__() == str(instance)
        assert instance.process_video_async() is None
