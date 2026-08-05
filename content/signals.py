from .models import Video
from content.tasks import convert_480p, convert_720p, convert_1080p
import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq
from django_rq import enqueue


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print("VIDEO GESPEICHERT - TASK GESTARTET")
    print("Video post save signal triggered")
    if created:
        print("New video created:", instance.title)
        # enqueue(convert_480p, instance.video_file.path)
        # queue = django_rq.get_queue("default", autocommit=True)
        # queue.enqueue(convert_480p, instance.video_file.path)
        # django_rq.enqueue(convert_480p, instance.video_file.path)
        django_rq.enqueue(convert_480p, instance.id)
        django_rq.enqueue(convert_720p, instance.id)
        # django_rq.enqueue(convert_1080p, instance.id)


@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
