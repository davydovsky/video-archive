from django.contrib import admin
from video_encoding.admin import FormatInline

from project.apps.video_archive.models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    Video file admin
    """
    inlines = (FormatInline,)
    list_dispaly = ('get_filename', 'width', 'height', 'duration')
    fields = ('file', 'width', 'height', 'duration', 'preview')
    readonly_fields = fields
