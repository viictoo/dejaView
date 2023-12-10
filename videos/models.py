from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from .utils import generate_thumbnail, generate_preview_clip
from django.db.models.signals import post_save
import os
import uuid
from moviepy.editor import VideoFileClip
import subprocess
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

    # def get_hls_url(self):
    #     return os.path.join('hls', f'{self.id}.m3u8')
    def get_hls_url(self):
        hls_file = f'{self.id}.m3u8'
        return f'{settings.MEDIA_URL}hls/{hls_file}'
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

        # Perform HLS transcoding
        # hls_output_dir = os.path.join('media', 'hls')
        # os.makedirs(hls_output_dir, exist_ok=True)
        # enc_key = os.path.join('static', 'blog/keys/enc_key')
        # print(enc_key)

        # hls_command = [
        #     'ffmpeg',
        #     '-i', self.video_file.path,
        #     '-hls_time', '9',
        #     '-hls_key_info_file', '/home/victorvc/myApp/you_app/key_info.txt',
        #     '-hls_playlist_type', 'vod',
        #     os.path.join(hls_output_dir, f'{self.id}.m3u8')
        # ]
        # subprocess.run(hls_command)

        def transcode_to_abr(video_path, output_dir, video_id):
            # List of bitrates and resolutions for ABR
            abr_settings = [
                {'bitrate': '500k', 'resolution': 'w=640:h=360'},
                {'bitrate': '1000k', 'resolution': 'w=1280:h=720'},
                # {'bitrate': '2000k', 'resolution': '1920x1080'},
            ]

            # Output HLS files for each ABR setting
            # for setting in abr_settings:
            # bitrate = setting['bitrate']
            # resolution = setting['resolution']
            hls_output_dir = os.path.join('media', 'hls')
            os.makedirs(hls_output_dir, exist_ok=True)

            # hls_output_dir = os.path.join(output_dir, f'abr_{bitrate}_{resolution}')
            # os.makedirs(hls_output_dir, exist_ok=True)

            # hls_command = [
            #     'ffmpeg',
            #     '-i', video_path[0],
            #     -filter_complex, "[0:v]split=3[v1][v2][v3]; [v1]copy[v1out]; [v2]scale=w=1280:h=720[v2out]; [v3]scale=w=640:h=360[v3out]",
            #     '-c:v', 'libx264',
            #     '-b:v', bitrate,
            #     '-vf', f'scale={resolution}',
            #     '-c:a', 'aac',
            #     '-b:a', '128k',
            #     '-hls_time', '9',
            #     '-hls_key_info_file', '/home/victorvc/myApp/you_app/key_info.txt',
            #     '-hls_playlist_type', 'vod',
            #     '-hls_segment_filename', os.path.join(hls_output_dir, f'{video_id}_%03d.ts'),
            #     os.path.join(hls_output_dir, f'{video_id}.m3u8')
            # ]
            hls1_command = [
                "ffmpeg",
                "-hide_banner", '-y',
                "-i", video_path[0],
                "-c:a", "aac",
                '-ar', "48000",
                '-c:v', "h264",
                "-profile:v", "main",
                "-crf", "19",
                '-sc_threshold', '0',
                '-g', '60',
                '-keyint_min', '60',
                '-hls_time', '10',
                '-hls_playlist_type', 'vod',
                '-vf', 'scale=w=426:h=-2',
                '-b:v', '400k',
                '-maxrate', '428k',
                '-bufsize', '600k',
                '-b:a', '128k',
                '-hls_segment_filename',
                os.path.join(hls_output_dir, f'{video_id}_%v/240p_%02d.ts'),
                '-c:a', 'aac',
                '-ar', '48000',
                '-c:v', 'h264',
                '-profile:v', "main",
                '-crf', '19',
                '-sc_threshold', '0',
                '-g', '60',
                '-keyint_min', '60',
                '-hls_time', '10',
                '-hls_playlist_type', 'vod',
                '-vf', 'scale=w=640:h=-2',
                '-b:v', '800k',
                '-maxrate', '856k',
                '-bufsize', '1200k',
                '-b:a', '128k',
                '-hls_segment_filename',
                                os.path.join(hls_output_dir, f'{video_id}_%v/360p_%03d.ts'),
                '-c:a', 'aac',
                '-ar', '48000',
                '-c:v', 'h264',
                '-profile:v', 'main',
                '-crf', '19',
                '-sc_threshold', '0',
                '-g', '60',
                '-keyint_min', '60',
                '-hls_time', '10',
                '-hls_playlist_type', 'vod',
                '-vf', 'scale=w=842:h=-2',
                '-b:v', '1400k',
                '-maxrate', '1498k',
                '-bufsize', '2100k',
                '-b:a', '128k',
                '-hls_segment_filename',
                os.path.join(hls_output_dir, f'{video_id}_%v/480p_%02d.ts'),
                '-c:a', 'aac',
                '-ar', '48000',
                '-c:v', 'h264',
                '-profile:v', 'main',
                '-crf', '19',
                '-sc_threshold', '0',
                '-g', '60',
                '-keyint_min', '60',
                '-hls_time', '10',
                '-hls_playlist_type', 'vod',
                '-vf', 'scale=w=1280:h=-2',
                '-b:v', '2800k',
                '-maxrate', '2996k',
                '-bufsize', '4200k',
                '-b:a', '128k',
                '-hls_segment_filename', os.path.join(hls_output_dir, f'{video_id}_%v/data%02d.ts',  os.path.join(hls_output_dir, f'{video_id}_480p/{video_id}.m3u8'))
            ]

            hls_command = [
                'ffmpeg',
                '-i', video_path[0],
                '-filter_complex', "[0:v]split=3[v1][v2][v3]; [v1]copy[v1out]; [v2]scale=w=1280:h=720[v2out]; [v3]scale=w=640:h=360[v3out]",
                '-map', "[v1out]",
                '-c:v:0', 'libx264',
                '-x264-params', "nal-hrd=cbr:force-cfr=1",
                '-b:v:0', '5M',
                '-maxrate:v:0', '2M',
                '-minrate:v:0', '2M',
                '-bufsize:v:0', '3M',
                '-preset', 'medium',
                '-g', '48',
                '-sc_threshold', '0',
                '-keyint_min', '48',
                '-map', "[v2out]",
                '-c:v:1', 'libx264',
                '-x264-params', "nal-hrd=cbr:force-cfr=1",
                '-b:v:1', '3M',
                '-maxrate:v:1', '1M',
                '-minrate:v:1', '1M',
                '-bufsize:v:1', '2M',
                '-preset', 'fast',
                '-g', '48',
                '-sc_threshold', '0',
                '-keyint_min', '48',
                '-map', "[v3out]",
                '-c:v:2', 'libx264',
                '-x264-params', "nal-hrd=cbr:force-cfr=1",
                '-b:v:2', '1M',
                '-maxrate:v:2', '500K',
                '-minrate:v:2', '500K',
                '-bufsize:v:2', '500K',
                '-preset', 'fast',
                '-g', '48',
                '-sc_threshold', '0',
                '-keyint_min', '48',
                '-map', 'a:0',
                '-c:a:0', 'aac',
                '-b:a:0', '96k',
                '-ac', '2',
                '-map', 'a:0',
                '-c:a:1', 'aac',
                '-b:a:1', '96k',
                '-ac', '2',
                '-map', 'a:0',
                '-c:a:2', 'aac',
                '-b:a:2', '48k',
                '-ac', '2',
                '-f', 'hls',
                '-hls_time', '6',
                '-hls_playlist_type', 'vod',
                '-hls_flags', 'independent_segments',
                '-hls_segment_type', 'mpegts',
                # '-hls_segment_filename', 'stream_%v/data%02d.ts',
                '-hls_segment_filename', os.path.join(hls_output_dir, f'{video_id}_%v/data%02d.ts'),
                '-hls_key_info_file', '/home/victorvc/myApp/you_app/key_info.txt',
                '-master_pl_name', f'{video_id}.m3u8',
                '-var_stream_map', "v:0,a:0,name:HQp v:1,a:1,name:720p v:2,a:2,name:360p",
                os.path.join(hls_output_dir, f'{video_id}_%v/{video_id}.m3u8'),
                # '-hls_segment_filename', os.path.join(hls_output_dir, f'{video_id}_%03d.ts'),
                # os.path.join(hls_output_dir, f'{video_id}.m3u8')
            ]

            subprocess.run(hls_command)

        # Example usage
        video_path = self.video_file.path,
        print(video_path[0])
        # output_dir = '/path/to/output/directory'
        output_dir = os.path.join('media', 'hls')
        video_id = self.id

        transcode_to_abr(video_path, output_dir, video_id)

# from chunkedUpload.models import ChunkedUpload

# class Video(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     upload_date = models.DateTimeField(auto_now_add=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     video_file = models.FileField(upload_to='videos/')
#     thumbnail = models.ImageField(
#         upload_to='thumbnails/', blank=True, null=True)
#     preview_clip = models.FileField(
#         upload_to='previews/', blank=True, null=True)

#     def __str__(self):
#         return self.title

# @receiver(post_save, sender=Video)
# def handle_video_upload(sender, instance, **kwargs):
#     if not instance.preview_clip:
#         # Assuming you have a function to generate a preview clip
#         video_path = instance.video_file.path
#         preview_clip_path = f'media/previews/preview_{instance.pk}.mp4'
#         generate_preview_clip(video_path, preview_clip_path)
#         instance.preview_clip.name = os.path.relpath(preview_clip_path, 'media')
#         instance.save(update_fields=['preview_clip'])
#     # Handle chunked video upload completion
#     chunked_uploads = ChunkedUpload.objects.filter(video=instance).order_by('sequence')
#     if chunked_uploads.exists() and chunked_uploads.last().sequence == instance.total_chunks:
#         complete_video_path = f'media/videos/{instance.pk}.mp4'
#         with open(complete_video_path, 'wb') as complete_video:
#             for chunked_upload in chunked_uploads:
#                 if chunked_upload.chunk:
#                     chunked_upload.chunk.open('rb')
#                     complete_video.write(chunked_upload.chunk.file.read())
#                     chunked_upload.chunk.close()
#                 chunked_upload.delete()

#         instance.video_file.name = os.path.relpath(complete_video_path, 'media')
#         instance.save(update_fields=['video_file'])
