from django.core.management.base import BaseCommand

from meinberlin.apps.bplan.models import Bplan
from meinberlin.apps.bplan.tasks import get_bplan_point


class Command(BaseCommand):
    help = (
        "Uses the Bplan identifier to get the coordinates "
        "from API of bplan-prod.liqd.net"
    )

    def handle(self, *args, **options):
        for bplan in Bplan.objects.all():
            if bplan.identifier:
                point = get_bplan_point(bplan.identifier)

                if point:
                    bplan.point = point
                bplan.save(update_fields=["point", "administrative_district"])
