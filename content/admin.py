from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "created_at")
    search_fields = ("title",)

    fields = (
        "title",
        "description",
        "category",
        "video_file",
    )

    class Media:
        js = ("content/js/upload_progress.js",)
