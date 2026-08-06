from .models import Video
from content.tasks import convert_480p, convert_720p, convert_1080p, convert_HLS
import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
from django_rq import enqueue


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("VIDEO GESPEICHERT - TASK GESTARTET")
    if created:
        # enqueue(convert_480p, instance.video_file.path)
        # queue = django_rq.get_queue("default", autocommit=True)
        # queue.enqueue(convert_480p, instance.video_file.path)
        # django_rq.enqueue(convert_480p, instance.video_file.path)
        django_rq.enqueue(convert_480p, instance.id)
        print("Video post 480p signal saved")
        django_rq.enqueue(convert_720p, instance.id)
        print("Video post 720p signal saved")
        django_rq.enqueue(convert_1080p, instance.id)
        print("Video post 1080p signal saved")
        django_rq.enqueue(convert_HLS, instance.id)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    if instance.video_file and os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)
    base_path, _ = os.path.splitext(instance.video_file.path)
    resolutions = ["480p", "720p", "1080p"]

    for res in resolutions:
        converted_file_path = f"{base_path}_{res}.mp4"
        if os.path.isfile(converted_file_path):
            os.remove(converted_file_path)

    for field_name in ["video_480p", "video_720p", "video_1080p"]:
        field = getattr(instance, field_name, None)
        if field and hasattr(field, "path") and os.path.isfile(field.path):
            os.remove(field.path)
