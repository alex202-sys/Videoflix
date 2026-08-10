from core import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
import shutil
import os
from .tasks import convert_video_to_hls
from .models import Video


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        django_rq.enqueue(convert_video_to_hls, instance.id, job_timeout=3600)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes the entire HLS folder (media/hls/<id>/), including all
    subfolders (480p, 720p, 1080p) and all MP4 files, when deleting
    via the admin interface.
    """

    hls_main_dir = os.path.join(settings.MEDIA_ROOT, "hls", str(instance.id))
    if os.path.exists(hls_main_dir) and "media" in hls_main_dir:
        try:
            shutil.rmtree(hls_main_dir)
        except Exception as e:
            print(f"Error deleting HLS folder {hls_main_dir}: {e}")

    # # 2. Thumbnail .jpg deleted (z.B. media/thumbnails/video_44.jpg)
    # if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
    #     try:
    #         os.remove(instance.thumbnail.path)
    #     except Exception as e:
    #         print(f"Fehler beim Löschen des Thumbnails: {e}")

    fields_to_clean = [
        instance.video_file,
        instance.video_hls,
        instance.thumbnail,
    ]
    for field in fields_to_clean:
        if field and field.name and os.path.isfile(field.path):
            try:
                os.remove(field.path)
            except Exception as e:
                print(f"Error deleting file {field.path}: {e}")
