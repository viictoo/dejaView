from django.shortcuts import render

# Create your views here.
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChunkedUpload

@csrf_exempt
def handle_chunked_upload(request):
    if request.method == 'POST':
        video_id = request.POST.get('video_id')
        sequence = int(request.POST.get('sequence'))
        chunk = request.FILES.get('file')

        # Save the chunk to the temporary location
        temp_file_path = f'temporary/{video_id}_chunk_{sequence}.mp4'
        with open(temp_file_path, 'ab') as temp_file:
            temp_file.write(chunk.read())

        if request.POST.get('end') == '1':
            # Merge chunks into the complete video file
            complete_video_path = f'media/videos/{video_id}.mp4'
            with open(complete_video_path, 'wb') as complete_video:
                for chunk_sequence in range(1, sequence + 1):
                    chunk_file_path = f'temporary/{video_id}_chunk_{chunk_sequence}.mp4'
                    with open(chunk_file_path, 'rb') as chunk_file:
                        complete_video.write(chunk_file.read())

                    # Delete the temporary chunk file
                    os.remove(chunk_file_path)

            # Create a ChunkedUpload instance
            ChunkedUpload.objects.create(
                video_id=video_id,
                chunk=None,
                sequence=sequence,
            )

            return JsonResponse({'status': 'success'})

        else:
            # Create a ChunkedUpload instance for the chunk
            ChunkedUpload.objects.create(
                video_id=video_id,
                chunk=chunk,
                sequence=sequence,
            )

            return JsonResponse({'status': 'chunk_received'})

    return JsonResponse({'status': 'error'})
