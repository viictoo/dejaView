from django.apps import AppConfig


class MpesaConfig(AppConfig):
    """Configuration for the 'mpesa' app.

    Args:
        AppConfig (type): Base class for application configuration.

    Attributes:
        name (str): The name of the app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mpesa'
