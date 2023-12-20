from django.urls import path
from .views import (UserVideoListView,
                    upload_video,
                    video_detail,
                    VideoListView,
                    VideoUpdateView,
                    VideoDeleteView,
                    video_playback,
                    video_search)


urlpatterns = [
    # path('', index, name='videos-index'),
    path('videos/<uuid:video_id>/', video_detail, name='video-detail'),
    path('videos/upload/', upload_video, name='video-upload'),
    path('videos/search', video_search, name='video-search'),
    path('videos/<uuid:video_id>/play', video_playback, name='video-playback'),
    path('', VideoListView.as_view(), name='videos-home'),
    path('user/<str:username>', UserVideoListView.as_view(), name='user-videos'),
    path('videos/<uuid:pk>/update', VideoUpdateView.as_view(), name='video-update'),
    path('videos/<uuid:pk>/delete', VideoDeleteView.as_view(), name='video-delete'),
]
