from django.db import models
from django.contrib.auth.models import User
from .utils import generate_thumbnail, generate_preview_clip, transcode_to_abr
from django.db.models.signals import post_save
import os
import uuid
from django.urls import reverse
from django.conf import settings


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(
        upload_to='thumbnails/', blank=True)
    preview_clip = models.FileField(
        upload_to='previews/', blank=True, null=True)


    def get_hls_url(self):
        hls_file = f'{self.id}.m3u8'
        return f'{settings.MEDIA_URL}hls/{hls_file}'
        # uncomment to use stream from AWS storage bucket
        # return f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/hls/{hls_file}'
    hls_url = property(get_hls_url)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.thumbnail:
            video_path = self.video_file.path
            thumbnail_path = os.path.join(
                'media', 'thumbnails', f'thumbnail_{self.pk}.jpg')
            generate_thumbnail(video_path, thumbnail_path)
            self.thumbnail.name = os.path.relpath(thumbnail_path, 'media')
            self.save(update_fields=['thumbnail'])


        if not self.preview_clip:
            video_path = self.video_file.path
            preview_clip_path = os.path.join(
                'media', 'previews', f'preview_{self.pk}.mp4')
            generate_preview_clip(video_path, preview_clip_path)
            self.preview_clip.name = os.path.relpath(
                preview_clip_path, 'media')
            self.save(update_fields=['preview_clip'])

        video_path = self.video_file.path,
        # output_dir = '/path/to/output/directory'
        output_dir = os.path.join('media', 'hls')
        video_id = self.id
        transcode_to_abr(video_path, output_dir, video_id)
