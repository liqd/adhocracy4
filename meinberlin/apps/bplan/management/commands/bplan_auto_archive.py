from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from meinberlin.apps.bplan import models as bplan_models


# TODO: this will become obsolete and can be removed once the transition to diplan is completed.
class Command(BaseCommand):
    help = "Archive finished bplan projects and delete old statements."

    def handle(self, *args, **options):
        bplans = bplan_models.Bplan.objects.filter(is_draft=False, is_diplan=False)
        for bplan in bplans:
            if bplan.has_finished and not bplan.is_archived:
                bplan.is_archived = True
                bplan.save(update_fields=["is_archived"])
                self.stdout.write("Archived bplan {}.".format(bplan.name))

        # Delete statements of archived projects
        # To prevent deleting statements that have not been sent by mail yet
        # only statements older then 48h are deleted.
        num_deleted, _ = (
            bplan_models.Statement.objects.filter(module__project__is_archived=True)
            .filter(created__lt=timezone.now() - timedelta(hours=48))
            .delete()
        )
        if num_deleted:
            self.stdout.write(
                "Deleted {} statements from archived bplans.".format(num_deleted)
            )
