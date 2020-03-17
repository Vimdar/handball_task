try:
    from django.apps import AppConfig

    class ResultsConfig(AppConfig):
        """Config."""

        name = 'results'
        label = 'results_endpoint'

    __all__ = ('ResultsConfig',)

except ImportError:
    pass
