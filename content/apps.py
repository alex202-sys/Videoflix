from django.apps import AppConfig


class ContentConfig(AppConfig):
    """Configuration for the 'content' app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "content"

    def ready(self):
        import content.signals
