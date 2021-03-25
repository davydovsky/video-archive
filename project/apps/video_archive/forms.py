from django import forms


class VideoFileForm(forms.Form):
    """Video file upload form"""

    video_file = forms.FileField(label='Select a video ', required=False)


class VideoURLForm(forms.Form):
    """Video URL upload form"""

    video_link = forms.URLField(label='Provide an url ', required=False,
                                widget=forms.TextInput(attrs={'width': '70'}))

