from django.apps import AppConfig


class ChatConfig(AppConfig):
    """
    Configuration for the Chat application.
    Attributes:
        default_auto_field (str): Specifies the type of auto-incrementing primary key to use for models in this app.
        name (str): The name of the application.
    Methods:
        ready(): Imports the signals module to connect signal handlers.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "chat"

    def ready(self):
        import chat.signals as _  # noqa: F401
