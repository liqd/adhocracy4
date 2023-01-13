from django.core.management.base import BaseCommand

from meinberlin.apps.bplan.models import Bplan
from meinberlin.apps.bplan.tasks import get_bplan_api_pk_to_a4_admin_district_dict
from meinberlin.apps.bplan.tasks import get_bplan_point_and_district_pk


class Command(BaseCommand):
    help = (
        "Uses the Bplan identifier to get the coordinates "
        "and the district from API of bplan-prod.liqd.net"
    )

    def handle(self, *args, **options):
        dis_dict = get_bplan_api_pk_to_a4_admin_district_dict()

        for bplan in Bplan.objects.all():
            if bplan.identifier:
                point, district_pk = get_bplan_point_and_district_pk(bplan.identifier)

                if district_pk:
                    bplan.administrative_district = dis_dict[district_pk]
                if point:
                    bplan.point = point
                bplan.save(update_fields=["point", "administrative_district"])
