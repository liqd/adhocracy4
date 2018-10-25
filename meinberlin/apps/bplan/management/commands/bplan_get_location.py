import json
import urllib.request

from django.core.management.base import BaseCommand

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from meinberlin.apps.bplan.models import Bplan


class Command(BaseCommand):
    help = ('Uses the Bplan identifier to get the coordinates '
            'and the district from API of bplan-prod.liqd.net')

    def handle(self, *args, **options):

        url_dis = 'https://bplan-prod.liqd.net/api/bezirke/'
        req = urllib.request.Request(url_dis)
        res = urllib.request.urlopen(req)
        res_body = res.read()
        res_json = json.loads(res_body.decode("utf-8"))

        dis_dict = {}
        dis_json = res_json.get('features')
        if dis_json:
            for district in dis_json:

                dis_model = AdministrativeDistrict.objects.filter(
                    name=district['properties']['name']
                )
                if dis_model:
                    dis_dict[district['properties']['pk']] = \
                        dis_model[0]
                else:
                    dis_dict[district['properties']['pk']] = ''

        for bplan in Bplan.objects.all():
            print(bplan.identifier)
            if bplan.identifier:
                url_poi = 'https://bplan-prod.liqd.net/api/bplan/points/' + \
                    '?bplan={}'.format(bplan.identifier.replace(' ', '%20'))
                try:
                    req = urllib.request.Request(url_poi)
                    res = urllib.request.urlopen(req)
                    res_body = res.read()
                    res_json = json.loads(res_body.decode("utf-8"))

                    features = res_json.get('features')
                    if features:
                        district_pk = features[0]['properties']['bezirk']
                        bplan.administrative_district = \
                            dis_dict[district_pk]
                        bplan.point = features[0]
                        bplan.save()

                except UnicodeEncodeError:
                    # catches bplan-identifiers with problematic chars
                    pass
