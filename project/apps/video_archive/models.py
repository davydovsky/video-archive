from django.contrib.contenttypes.fields import GenericRelation
from django.db import models, transaction
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel
from video_encoding.fields import VideoField
from video_encoding.models import Format

from project.apps.video_archive import tasks


class Video(TimeStampedModel):
    """Video file storage."""

    width = models.PositiveIntegerField(editable=False, null=True, verbose_name=_('Width'))
    height = models.PositiveIntegerField(editable=False, null=True, verbose_name=_('Height'))
    duration = models.FloatField(editable=False, null=True, verbose_name=_('Duration'))

    file = VideoField(width_field='width', height_field='height', duration_field='duration')
    preview = models.ImageField(blank=True, verbose_name=_('Preview'))

    format_set = GenericRelation(Format)

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Video')

    def __str__(self) -> str:
        return f'{self.id}'

    def save(self, **kwargs) -> None:
        super().save(**kwargs)
        transaction.on_commit(self._process_video_async)  # process video upon saving in database

    def _process_video_async(self) -> None:
        """
        Process video using async worker.
         - create video preview
         - encode video in all supported formats
        :return: None
        """
        app_label = self._meta.app_label
        model_name = self._meta.model_name
        tasks.create_preview.delay(self.pk)
        tasks.convert_all_videos.delay(app_label, model_name, self.pk)
