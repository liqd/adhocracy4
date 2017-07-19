from django.core.management.base import BaseCommand

from meinberlin.apps.bplan import models as bplan_models


class Command(BaseCommand):
    help = 'Unpublish finished bplan projects.'

    def handle(self, *args, **options):
        bplans = bplan_models.Bplan.objects.filter(is_draft=False)
        for bplan in bplans:
            if bplan.has_finished:
                bplan.is_draft = True
                bplan.save()
                self.stdout.write('Unpublished bplan {}.'.format(bplan.name))
