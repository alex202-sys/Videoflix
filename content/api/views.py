from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.http import FileResponse, HttpResponse, StreamingHttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
import os
import re
from .serializers import VideoSerializer
from content.models import Video


class VideoListView(ListCreateAPIView):
    """
    GET /api/video/       - Lists all available videos
    POST /api/video/      - Creates/uploads a new video
    """

    queryset = Video.objects.all().order_by("-created_at")
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


class VideoDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET /api/video/<pk>/    - Retrieve details of a single video
    PUT/PATCH /api/video/<pk>/ - Update video
    DELETE /api/video/<pk>/ - Delete video
    """

    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


class VideoStreamView(APIView):
    """
    GET /api/video/<pk>/stream/ - Streams the video file with support for HTTP Range requests.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        video = get_object_or_404(Video, pk=pk)

        selected_file = video.video_file

        if not selected_file or not selected_file.name:
            raise Http404("Video file is not available.")

        file_path = selected_file.path
        if not os.path.exists(file_path):
            raise Http404("File not found on the server.")

        file_size = os.path.getsize(file_path)

        # HTTP 206 Partial Content
        range_header = request.META.get("HTTP_RANGE", "").strip()
        range_match = re.match(r"bytes=(\d+)-(\d+)?", range_header)

        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
        else:
            start = 0
            end = file_size - 1

        length = end - start + 1

        def file_iterator(file_name, chunk_size=8192, offset=start, length=length):
            with open(file_name, "rb") as f:
                f.seek(offset)
                remaining = length
                while remaining > 0:
                    bytes_to_read = min(chunk_size, remaining)
                    data = f.read(bytes_to_read)
                    if not data:
                        break
                    remaining -= len(data)
                    yield data

        response = StreamingHttpResponse(
            file_iterator(file_path),
            status=206 if range_header else 200,
            content_type="video/mp4",
        )
        response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        response["Accept-Ranges"] = "bytes"
        response["Content-Length"] = str(length)
        return response


class HLSResolutionPlaylistView(APIView):
    """
    GET /api/video/<movie_id>/<resolution>/index.m3u8
    Returns the m3u8 playlist for the specified resolution.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution=None, format=None):
        """Retrieve the HLS playlist for the specified resolution."""
        video = get_object_or_404(Video, pk=movie_id)

        if not video.video_hls or not video.video_hls.name:
            raise Http404("No HLS video available.")

        # Look for the path in the folder media/videos/hls/<movie_id>/<resolution>/index.m3u8
        # or adjusted to your file structure:
        # 1. Preferred path: subfolder media/hls/<movie_id>/<resolution>/index.m3u8
        base_dir = os.path.dirname(video.video_file.path) if video.video_file else ""
        playlist_path = os.path.join(
            base_dir, "hls", str(movie_id), resolution, "index.m3u8"
        )
        # Alternativ falls hls direkt im Feld gespeichert ist:
        if not os.path.exists(playlist_path) and video.video_hls:
            hls_dir = os.path.dirname(video.video_hls.path)
            playlist_path = os.path.join(hls_dir, resolution, "index.m3u8")
            resolution_playlist = (
                playlist_path if os.path.exists(playlist_path) else video.video_hls.path
            )

        if not os.path.exists(resolution_playlist):
            raise Http404(f"HLS playlist for {resolution} not found.")

        with open(resolution_playlist, "r", encoding="utf-8") as f:
            content = f.read()

        return HttpResponse(content, content_type="application/vnd.apple.mpegurl")


class HLSSegmentView(APIView):
    """
    GET /api/video/<movie_id>/<resolution>/<filename>
    Returns the individual .ts segment files for the HLS stream.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id, resolution, filename, format=None):
        video = get_object_or_404(Video, pk=movie_id)

        if video.video_hls:
            hls_dir = os.path.dirname(video.video_hls.path)
            sub_path = os.path.join(hls_dir, resolution, filename)
            segment_path = (
                sub_path
                if os.path.exists(sub_path)
                else os.path.join(hls_dir, filename)
            )
        else:
            base_dir = os.path.dirname(video.video_file.path)
            segment_path = os.path.join(
                base_dir, "hls", str(movie_id), resolution, filename
            )

        if not os.path.exists(segment_path) or not filename.endswith(".ts"):
            raise Http404("Segment not found.")

        return FileResponse(open(segment_path, "rb"), content_type="video/MP2T")
