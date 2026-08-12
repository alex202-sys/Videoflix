from core import settings
from django.apps import apps
from content.models import Video
import subprocess
import os

RESOLUTIONS = {
    "480p": {
        "scale": "scale=-2:480",
        "bitrate": "800k",
        "audio_bitrate": "96k",
    },
    "720p": {
        "scale": "scale=-2:720",
        "bitrate": "2500k",
        "audio_bitrate": "128k",
    },
    "1080p": {
        "scale": "scale=-2:1080",
        "bitrate": "5000k",
        "audio_bitrate": "192k",
    },
}


def convert_video_to_hls(video_id):
    """
    Creates actual resolution subfolders for an uploaded video
    under media/hls/<video_id>/<resolution>/ containing index.m3u8 and .ts segments,
    as well as automatically generating a thumbnail (screenshot) at the 1-second mark.
    """
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return

    source_path = video.video_file.path

    try:
        thumbnail_dir = os.path.join(settings.MEDIA_ROOT, "thumbnails")
        os.makedirs(thumbnail_dir, exist_ok=True)

        thumbnail_filename = f"video_{video.id}.jpg"
        thumbnail_path = os.path.join(thumbnail_dir, thumbnail_filename)

        cmd_thumb = [
            "ffmpeg",
            "-ss",
            "00:00:01",
            "-i",
            source_path,
            "-vframes",
            "1",
            "-q:v",
            "2",
            "-y",
            thumbnail_path,
        ]
        subprocess.run(cmd_thumb, check=True)

        video.thumbnail = f"thumbnails/{thumbnail_filename}"
        video.save(update_fields=["thumbnail"])
    except Exception as e:
        print(f"Fehler beim Erstellen des Thumbnails für Video {video_id}: {e}")

    base_hls_dir = os.path.join(settings.MEDIA_ROOT, "hls", str(video.id))

    for res_name, config in RESOLUTIONS.items():
        res_dir = os.path.join(base_hls_dir, res_name)
        os.makedirs(res_dir, exist_ok=True)

        m3u8_output = os.path.join(res_dir, "index.m3u8")
        segment_pattern = os.path.join(res_dir, "segment_%03d.ts")

        cmd_hls = [
            "ffmpeg",
            "-i",
            source_path,
            "-vf",
            config["scale"],
            "-c:v",
            "libx264",
            "-b:v",
            config["bitrate"],
            "-c:a",
            "aac",
            "-b:a",
            config["audio_bitrate"],
            "-hls_time",
            "6",
            "-hls_playlist_type",
            "vod",
            "-hls_segment_filename",
            segment_pattern,
            "-y",
            m3u8_output,
        ]
        subprocess.run(cmd_hls, check=True)

    rel_hls_path = os.path.relpath(
        os.path.join(base_hls_dir, "720p", "index.m3u8"), settings.MEDIA_ROOT
    )
    video.video_hls = rel_hls_path
    video.save()
