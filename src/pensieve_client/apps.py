# src/pensieve_client/apps.py

from django.apps import AppConfig

class PensieveClientConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pensieve_client'
    verbose_name = 'Pensieve APM'