from django.apps import AppConfig


class AppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification_be.apps'

    def ready(self):
        import notification_be.apps.signals
