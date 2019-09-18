from django.apps import AppConfig
from django.db.models.signals import post_migrate

from condottieri_profiles.signals import handlers

class CondottieriProfilesConfig(AppConfig):
    name = 'condottieri_profiles'
    verbose_name = 'Condottieri Profiles'

    def ready(self):
        from . import defaults
        from django.conf import settings
        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))
        post_migrate.connect(handlers.create_notice_types, sender=self)
