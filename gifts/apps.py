from django.apps import AppConfig


class GiftsConfig(AppConfig):
    """
    Configuration for the Gifts application.
    Attributes:
        default_auto_field (str): Specifies the type of auto-incrementing primary key to use for models in this app.
        name (str): The name of the application.
    Methods:
        ready(): Imports the signals module to connect signal handlers.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "gifts"

    def ready(self):
        import gifts.signals as _  # noqa: F401
