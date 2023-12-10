from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration for the 'users' app.

    Args:
        AppConfig (type): Base class for application configuration.

    Attributes:
        name (str): The name of the app.
    """
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """Registers signals when the application is ready.
        """
        import users.signals
