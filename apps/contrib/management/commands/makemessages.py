from os import path
from django.core.management.commands import makemessages


def get_module_dir(name):
    module = __import__(name)
    return path.dirname(module.__file__)


class Command(makemessages.Command):
    msgmerge_options = (
        makemessages.Command.msgmerge_options + ['--no-fuzzy-matching']
    )

    def handle(self, *args, **options):
        if options['domain'] == 'djangojs':
            if options['extensions'] is None:
                options['extensions'] = ['js', 'jsx']
        return super().handle(*args, **options)

    def find_files(self, root):
        a4_paths = super().find_files(get_module_dir('adhocracy4'))
        apps_paths = super().find_files(path.relpath(get_module_dir('apps')))
        meinberlin_paths = super().find_files(
            path.relpath(get_module_dir('meinberlin'))
        )

        return a4_paths + apps_paths + meinberlin_paths
