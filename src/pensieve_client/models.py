# src/pensieve_client/models.py

from django.contrib.auth.models import Group

# This is a proxy model. It uses the existing Project model from Django's auth app
# but allows us to attach our own custom admin to it.
class MonitoredProject(Group):
    class Meta:
        proxy = True
        verbose_name = 'Pensieve Dashboard'
        verbose_name_plural = 'Pensieve Dashboards'
        managed = False
