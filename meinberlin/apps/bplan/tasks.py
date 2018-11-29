import json
import urllib

from background_task import background

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from meinberlin.apps.bplan.models import Bplan


@background(schedule=0)
def get_location_information(bplan_id):
    bplan = Bplan.objects.get(pk=bplan_id)
    url_poi = 'https://bplan-prod.liqd.net/api/bplan/points/' + \
        '?bplan={}'.format(bplan.identifier.replace(' ', '%20'))
    url_dis = 'https://bplan-prod.liqd.net/api/bezirke/'

    try:
        req = urllib.request.Request(url_poi)
        res = urllib.request.urlopen(req)
        res_body = res.read()
        res_json = json.loads(res_body.decode("utf-8"))

        features = res_json.get('features')
        if features:
            district_pk = features[0]['properties']['bezirk']

            req = urllib.request.Request(url_dis)
            res = urllib.request.urlopen(req)
            res_body = res.read()
            res_json = json.loads(res_body.decode("utf-8"))

            dis_json = res_json.get('features')
            if dis_json:
                for district in dis_json:
                    if district['properties']['pk'] == district_pk:
                        dis_model = AdministrativeDistrict.objects.filter(
                            name=district['properties']['name']
                        )
                        if dis_model:
                            bplan.administrative_district = \
                                dis_model[0]
                        else:
                            bplan.administrative_district = None

            bplan.point = features[0]
            bplan.save(update_fields=['point', 'administrative_district'])

    except UnicodeEncodeError:
        # catches bplan-identifiers with problematic chars
        pass
