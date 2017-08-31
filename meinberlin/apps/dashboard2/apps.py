from django.apps import AppConfig


class Config(AppConfig):
    name = 'meinberlin.apps.dashboard2'
    label = 'meinberlin_dashboard2'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('dashboard', register_to=self.module.components)

        from . import signals
        signals.connect_model_signal_handlers()
