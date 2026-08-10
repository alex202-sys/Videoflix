from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titel")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    category = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Category"
    )

    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)

    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="Creation time"
    )

    video_file = models.FileField(
        upload_to="videos/", blank=True, null=True, verbose_name="Video-file"
    )
    video_hls = models.FileField(
        upload_to="videos/", blank=True, null=True, verbose_name="HLS Video"
    )

    def __str__(self):
        return self.title
