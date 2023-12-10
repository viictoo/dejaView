from django import forms
import os
import magic
from .models import Video
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from moviepy.video.io.VideoFileClip import VideoFileClip
from .utils import generate_thumbnail

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'price', 'video_file']


    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        print("WWWWWWWWWWWWWWWW", vars(video_file))

        if video_file.file != None:
            print("=================",vars(video_file))
            content_type = video_file.content_type.split('/')[0]
            if content_type not in ['video']:
                raise ValidationError(_('File is not a video'))

        return video_file

    # def clean_video_file(self):
    #     video_file = self.cleaned_data.get('video_file')

    #     # Check if the uploaded file is a video
    #     allowed_extensions = ['mp4', 'avi', 'mov', 'mkv']  # allowed extensions
    #     if not any(video_file.name.lower().endswith(ext) for ext in allowed_extensions):
    #         raise ValidationError('Invalid file type. Please upload a valid video file.')

    #     # Check if the video is longer than 5 seconds
    #     try:
    #         print(video_file.content_type)
    #         with VideoFileClip(video_file.path) as video:
    #             duration = video.duration
    #             if duration <= 30:
    #                 raise ValidationError('The video must be longer than 30 seconds.')
    #     except Exception as e:
    #         print(e)
    #         raise ValidationError('Error processing the video file.')

    #     return video_file
