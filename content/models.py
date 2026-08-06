from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titel")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Upload time")
    video_file = models.FileField(
        upload_to="videos/", blank=True, null=True, verbose_name="Video-file"
    )
    # Neue Felder für konvertierte Versionen:
    video_480p = models.FileField(upload_to="videos/", blank=True, null=True)
    video_720p = models.FileField(upload_to="videos/", blank=True, null=True)
    video_1080p = models.FileField(upload_to="videos/", blank=True, null=True)
    video_hls = models.FileField(
        upload_to="videos/", blank=True, null=True, verbose_name="HLS Video"
    )

    def __str__(self):
        return self.title
