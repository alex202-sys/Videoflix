from rest_framework import serializers
from content.models import Video


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "video_file",
            "video_480p",
            "video_720p",
            "video_1080p",
        ]
