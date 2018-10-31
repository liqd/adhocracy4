from django.apps import AppConfig


class Config(AppConfig):
    name = 'adhocracy4.dashboard'
    label = 'a4dashboard'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('dashboard', register_to=self.module.components)
        self.module.components.apply_replacements()
