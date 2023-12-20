import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image
import os
import subprocess

def generate_thumbnail(video_path, output_path):
    try:
        with VideoFileClip(video_path) as video:
            # Get a list of frames from the video
            frames = [video.get_frame(t) for t in range(
                0, min(int(video.duration), 20), 1)]

            # Calculate the variance of each frame
            variances = [np.var(frame) for frame in frames]

            # Find the index of the frame with the highest variance
            best_frame_index = np.argmax(variances)

            # Use the frame with the highest variance as the thumbnail

            clip = VideoFileClip(video_path)
            frame = clip.get_frame(best_frame_index)
            clip.close()

            thumbnail = Image.fromarray(frame)
            thumbnail.save(output_path)
    except Exception as e:
        print(f"Error generating thumbnail: {e}")


def generate_preview_clip(video_path, output_path):
    try:
        with VideoFileClip(video_path) as video:
            preview_clip = video.subclip(5, 25)
            preview_clip.write_videofile(
                output_path, codec="libx264", bitrate="500k", preset="medium")
    except Exception as e:
        print(f"Error generating preview clip: {e}")


def transcode_to_abr(video_path, output_dir, video_id):
    hls_output_dir = os.path.join('media', 'hls')
    os.makedirs(hls_output_dir, exist_ok=True)

    hls_command = [
        'ffmpeg',
        '-i', video_path[0],
        # map the output to  three different renditions: copy, 720p, 360p
        '-filter_complex',
        "[0:v]split=3[v1][v2][v3]; [v1]copy[v1out]; [v2]scale=w=1280:h=720[v2out]; [v3]scale=w=640:h=360[v3out]",
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
        '-hls_segment_filename', os.path.join(
            hls_output_dir, f'{video_id}_%v/data%02d.ts'),
        '-hls_key_info_file', '/home/victorvc/myApp/you_app/key_info.txt',
        '-master_pl_name', f'{video_id}.m3u8',
        '-var_stream_map',
        "v:0,a:0,name:HQp v:1,a:1,name:720p v:2,a:2,name:360p",
        os.path.join(hls_output_dir, f'{video_id}_%v/{video_id}.m3u8'),
    ]
    # run ffmpeg binaries
    subprocess.run(hls_command)
