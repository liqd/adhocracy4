import json
import urllib.request

from django.core.management.base import BaseCommand

from meinberlin.apps.bplan.models import Bplan


class Command(BaseCommand):
    help = ('Uses the Bplan identifier to get the location '
            'information from API of bplan-prod.liqd.net')

    def handle(self, *args, **options):

        for bplan in Bplan.objects.all():
            print(bplan.identifier)
            if bplan.identifier:
                url = 'https://bplan-prod.liqd.net/api/bplan/points/' + \
                    '?bplan={}'.format(bplan.identifier.replace(' ', '%20'))
                req = urllib.request.Request(url)
                res = urllib.request.urlopen(req)
                res_body = res.read()
                res_json = json.loads(res_body.decode("utf-8"))

                features = res_json.get('features')
                if features:
                    geometry = features[0].get('geometry')
                    print(geometry)

                    if geometry:
                        coordinates = geometry.get('coordinates')
                        print(coordinates)
