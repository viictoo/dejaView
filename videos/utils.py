import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image




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
            preview_clip.write_videofile(output_path, codec="libx264", bitrate="500k", preset="medium")
    except Exception as e:
        print(f"Error generating preview clip: {e}")


# def generate_thumbnail(video_path, output_path):
#     try:
#         with VideoFileClip(video_path) as video:
#             # Get a list of frames from the video
#             # frames = [video.get_frame(t) for t in range(0, int(video.duration), 1)]
#             frames = [video.get_frame(t) for t in range(
#                 0, min(int(video.duration), 20), 1)]

#             # Calculate the variance of each frame
#             variances = [np.var(frame) for frame in frames]

#             # Find the index of the frame with the highest variance
#             best_frame_index = np.argmax(variances)

#             # Use the frame with the highest variance as the thumbnail
#             # best_frame = frames[best_frame_index]
#             # print(best_frame_index)
#             # print(best_frame.shape)
#             # print(best_frame.dtype)
#             # print(best_frame.ndim)

#             clip = VideoFileClip(video_path)
#             frame = clip.get_frame(best_frame_index)
#             clip.close()

#             thumbnail = Image.fromarray(frame)
#             thumbnail.save(output_path)

#             # # Determine the color mode based on the structure of best_frame
#             # color_mode = 'RGB' if best_frame.ndim == 3 else 'L'

#             # thumbnail = Image.fromarray((best_frame * 255).astype('uint8'), color_mode)
#             # # thumbnail.save(output_path, format='webp')
#             # thumbnail.save(output_path, format='jpeg')
#     except Exception as e:
#         print(f"Error generating thumbnail: {e}")

# def generate_thumbnail(video_path, thumbnail_path):
#     clip = VideoFileClip(video_path)
#     frame = clip.get_frame(2)  # Get a frame from 2-second mark
#     clip.close()

#     thumbnail = Image.fromarray(frame)
#     thumbnail.save(thumbnail_path)

# def generate_thumbnail(video_path, output_path):
#     try:
#         with VideoFileClip(video_path) as video:
#             frame = video.get_frame(0)  # Get the first frame of the video
#             thumbnail = Image.fromarray((frame * 255).astype('uint8'))
#             thumbnail.save(output_path, format='webp')
#     except Exception as e:
#         print(f"Error generating thumbnail: {e}")


# def generate_thumbnail(video_path, output_path):
#     try:
#         with VideoFileClip(video_path) as video:
#             # Get a list of frames from the video
#             frames = [video.get_frame(t) for t in range(0, int(video.duration), 1)]

#             # Calculate the variance of each frame
#             variances = [np.var(frame) for frame in frames]

#             # Find the index of the frame with the highest variance
#             best_frame_index = np.argmax(variances)

#             # Use the frame with the highest variance as the thumbnail
#             best_frame = frames[best_frame_index]
#             thumbnail = Image.fromarray((best_frame * 255).astype('uint8'))
#             thumbnail.save(output_path, format='webp')

#     except Exception as e:
#         print(f"Error generating thumbnail: {e}")
