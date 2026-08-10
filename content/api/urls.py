from django.urls import path
from .views import (
    HLSResolutionPlaylistView,
    VideoListView,
    VideoDetailView,
    HLSSegmentView,
    VideoStreamView,
)

urlpatterns = [
    path("video/", VideoListView.as_view(), name="video-list"),
    path("video/<int:pk>/", VideoDetailView.as_view(), name="video-detail"),
    path("video/<int:pk>/stream/", VideoStreamView.as_view(), name="video-stream"),
    path(
        "video/<int:movie_id>/<str:resolution>/index.m3u8",
        HLSResolutionPlaylistView.as_view(),
        name="hls-resolution-playlist",
    ),
    path(
        "video/<int:movie_id>/<str:resolution>/<str:filename>",
        HLSSegmentView.as_view(),
        name="hls-segment",
    ),
]
