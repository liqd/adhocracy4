from django.core.management.base import BaseCommand

from meinberlin.apps.bplan import models as bplan_models


class Command(BaseCommand):
    help = 'Archive finished bplan projects.'

    def handle(self, *args, **options):
        bplans = bplan_models.Bplan.objects.filter(is_draft=False)
        for bplan in bplans:
            if bplan.has_finished:
                bplan.is_archived = True
                bplan.save()
                self.stdout.write('Archived bplan {}.'.format(bplan.name))
