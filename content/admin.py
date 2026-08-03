from django.contrib import admin
from .models import Video


# Register your models here.
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "upload_date")
    search_fields = ("title",)
