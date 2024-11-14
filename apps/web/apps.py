from django.apps import AppConfig


class WebportalConfig(AppConfig):
    name = 'apps.web'

    def ready(self):
        import apps.web.signals