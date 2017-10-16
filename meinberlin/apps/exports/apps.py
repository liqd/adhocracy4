from django.apps import AppConfig


class Config(AppConfig):
    name = 'meinberlin.apps.exports'
    label = 'meinberlin_exports'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('exports', register_to=self.module.exports)
