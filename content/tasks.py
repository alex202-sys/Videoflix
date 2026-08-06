from core import settings
from django.apps import apps
import subprocess
import os

# def convert_480p(source_file_path):
#     # Beispiel: /app/media/videos/mein_video.mp4 -> /app/media/videos/mein_video_480p.mp4
#     base_path, _ = os.path.splitext(source_file_path)
#     target = f"{base_path}_480p.mp4"

#     # Als Liste definieren & '-y' erzwingt das Überschreiben ohne Hängenbleiben
#     cmd = [
#         "ffmpeg",
#         "-y",
#         "-i",
#         source_file_path,
#         "-vf",
#         "scale=-2:480",  # -2 stellt sicher, dass Breite & Höhe durch 2 teilbar sind (Standard für H.264/MP4)
#         "-c:v",
#         "libx264",  # x264 ist moderner und kompatibler als mpeg4
#         "-crf",
#         "23",
#         "-c:a",
#         "aac",
#         target,
#     ]

#     subprocess.run(cmd, check=True)


def convert_480p(video_id):
    Video = apps.get_model("content", "Video")
    video = Video.objects.get(pk=video_id)

    source_path = video.video_file.path
    base_path, _ = os.path.splitext(source_path)
    target_path = f"{base_path}_480p.mp4"

    # FFmpeg Ausführung
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        source_path,
        "-vf",
        "scale=-2:480",
        "-c:v",
        "libx264",
        "-crf",
        "23",
        "-c:a",
        "aac",
        target_path,
    ]
    subprocess.run(cmd, check=True)

    # Relativen Pfad für Django berechnen & im Model speichern
    relative_path = os.path.relpath(target_path, settings.MEDIA_ROOT)
    video.video_480p = relative_path
    video.save(update_fields=["video_480p"])


# Variante für 720p und 1080p könnte ähnlich aussehen, z.B.:
def convert_720p(video_id):
    Video = apps.get_model("content", "Video")
    video = Video.objects.get(pk=video_id)

    source_path = video.video_file.path
    base_path, _ = os.path.splitext(source_path)
    target_path = f"{base_path}_720p.mp4"

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        source_path,
        "-vf",
        "scale=-2:720",
        "-c:v",
        "libx264",
        "-crf",
        "23",
        "-c:a",
        "aac",
        target_path,
    ]
    subprocess.run(cmd, check=True)

    relative_path = os.path.relpath(target_path, settings.MEDIA_ROOT)
    video.video_720p = relative_path
    video.save(update_fields=["video_720p"])


def convert_1080p(video_id):
    Video = apps.get_model("content", "Video")
    video = Video.objects.get(pk=video_id)

    source_path = video.video_file.path
    base_path, _ = os.path.splitext(source_path)
    target_path = f"{base_path}_1080p.mp4"

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        source_path,
        "-vf",
        "scale=-2:1080",
        "-c:v",
        "libx264",
        "-crf",
        "23",
        "-c:a",
        "aac",
        target_path,
    ]
    subprocess.run(cmd, check=True)

    relative_path = os.path.relpath(target_path, settings.MEDIA_ROOT)
    video.video_1080p = relative_path
    video.save(update_fields=["video_1080p"])


def convert_HLS(video_id):
    Video = apps.get_model("content", "Video")
    video = Video.objects.get(pk=video_id)

    source_path = video.video_file.path
    base_path, _ = os.path.splitext(source_path)

    output_dir = f"{base_path}_hls"
    os.makedirs(output_dir, exist_ok=True)
    target_m3u8 = os.path.join(output_dir, "index.m3u8")
    segment_pattern = os.path.join(output_dir, "segment_%03d.ts")

    cmd = [
        "ffmpeg",
        "-i",
        source_path,
        "-codec",
        "copy",
        "-start_number",
        "0",
        "-hls_time",
        "10",
        "-hls_list_size",
        "0",
        "-hls_segment_filename",
        segment_pattern,
        "-f",
        "hls",
        target_m3u8,
    ]
    subprocess.run(cmd, check=True)

    relative_path = os.path.relpath(target_m3u8, settings.MEDIA_ROOT)
    video.refresh_from_db()
    video.video_hls = relative_path
    video.save(update_fields=["video_hls"])
