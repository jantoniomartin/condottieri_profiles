from django.apps import AppConfig
from django.db.models.signals import post_migrate

from condottieri_profiles.signals import handlers

class CondottieriProfilesConfig(AppConfig):
    name = 'condottieri_profiles'
    verbose_name = 'Condottieri Profiles'

    def ready(self):
        post_migrate.connect(handlers.create_notice_types, sender=self)
