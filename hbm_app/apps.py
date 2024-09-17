from django.apps import AppConfig


class HbmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hbm_app'

    def ready(self):
        import hbm_app.signals # noqa
