from django.apps import AppConfig


class AuthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'
    verbose_name = 'Authentication and User Management'

    def ready(self):
        """
        Import signals when the app is ready.
        This ensures user-related events (like creating a profile after registration)
        are automatically handled.
        """
        try:
            import authapp.signals  # noqa: F401
        except ImportError:
            pass
