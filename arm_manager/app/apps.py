from django.apps import AppConfig as config


class AppConfig(config):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
