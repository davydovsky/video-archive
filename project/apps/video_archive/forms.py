from django import forms


class VideoFileForm(forms.Form):
    """Video file upload form."""

    video_file = forms.FileField(label='Select a video file', required=False,
                                 widget=forms.FileInput(attrs={'accept': 'video/*'}))


class VideoURLForm(forms.Form):
    """Video URL upload form."""

    video_link = forms.URLField(label='Provide an url', required=False)
