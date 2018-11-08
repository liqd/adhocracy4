import json
import urllib

from background_task import background

from meinberlin.apps.bplan.models import Bplan


@background(schedule=0)
def get_location_information(bplan_id):
    bplan = Bplan.objects.get(pk=bplan_id)
    url_poi = 'https://bplan-prod.liqd.net/api/bplan/points/' + \
        '?bplan={}'.format(bplan.identifier.replace(' ', '%20'))
    try:
        req = urllib.request.Request(url_poi)
        res = urllib.request.urlopen(req)
        res_body = res.read()
        res_json = json.loads(res_body.decode("utf-8"))

        features = res_json.get('features')
        if features:
            bplan.point = features[0]
            bplan.save()

    except UnicodeEncodeError:
        # catches bplan-identifiers with problematic chars
        pass
