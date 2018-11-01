from django.apps import AppConfig


class Config(AppConfig):
    name = 'adhocracy4.phases'
    label = 'a4phases'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('phases', register_to=self.module.content)
