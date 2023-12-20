from django import forms
from .models import Video
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'price', 'video_file']


    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')

        if video_file.file != None:
            content_type = video_file.content_type.split('/')[0]
            if content_type not in ['video']:
                raise ValidationError(_('File is not a video'))

        return video_file
