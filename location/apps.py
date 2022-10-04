from django.apps import AppConfig


class LocationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "location"
    verbose_name = "Location Models"

    def ready(self):
        import location.signals  # noqa
