from rest_framework import serializers
from content.models import Video
import os


class VideoSerializer(serializers.ModelSerializer):
    description = serializers.CharField(default="No description available")
    category = serializers.CharField(default="Generally categorized")
    created_at = serializers.DateTimeField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            "id",
            "created_at",
            "title",
            "description",
            "thumbnail_url",
            "category",
            "video_file",
            "video_hls",
        ]

    def get_thumbnail_url(self, obj):

        request = self.context.get("request")
        if obj.thumbnail:
            if request is not None:
                return request.build_absolute_uri(obj.thumbnail.url)
            return f"http://127.0.0.1:8000{obj.thumbnail.url}"

        # 2. Fallback: Wenn noch kein Bild generiert wurde -> default.jpg
        default_path = "/media/thumbnails/default.jpg"
        if request is not None:
            return request.build_absolute_uri(default_path)
        return f"http://127.0.0.1:8000{default_path}"
