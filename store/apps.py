from django.apps import AppConfig


class StoreConfig(AppConfig):
    """Configuration for the store application."""

    name = 'store'

    def ready(self):
        """Load signals when the application starts."""
        import store.signals
