import json
import logging
import urllib

from celery import shared_task

from adhocracy4.administrative_districts.models import AdministrativeDistrict
from meinberlin.apps.bplan.models import Bplan

logger = logging.getLogger(__name__)


def get_features_from_bplan_api(endpoint):
    url = "https://bplan-prod.liqd.net/api/" + endpoint
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    res_body = res.read()
    res_json = json.loads(res_body.decode("utf-8"))

    return res_json.get("features")


def get_bplan_point_and_district_pk(bplan_identifier):
    url_poi = "bplan/points/" + "?bplan={}".format(bplan_identifier.replace(" ", "%20"))

    try:
        features = get_features_from_bplan_api(url_poi)
        if features:
            district_pk = features[0]["properties"]["bezirk"]
            point = features[0]

            return point, district_pk

        return None, None

    except UnicodeEncodeError:
        # catches bplan-identifiers with problematic chars
        return None, None


def get_bplan_api_pk_to_a4_admin_district_dict():
    url_dis = "bezirke/"
    features = get_features_from_bplan_api(url_dis)
    dis_dict = {}
    if features:
        for district in features:
            dis_model = AdministrativeDistrict.objects.filter(
                name=district["properties"]["name"]
            )
            if dis_model:
                dis_dict[district["properties"]["pk"]] = dis_model[0]
            else:
                dis_dict[district["properties"]["pk"]] = None

    return dis_dict


@shared_task
def get_location_information(bplan_id):
    bplan = Bplan.objects.get(pk=bplan_id)
    point, district_pk = get_bplan_point_and_district_pk(bplan.identifier)

    if district_pk:
        dis_dict = get_bplan_api_pk_to_a4_admin_district_dict()
        bplan.administrative_district = dis_dict[district_pk]
        bplan.point = point
    else:
        logger.error(
            "The identifier '{}' for bplan '{}' seems to be wrong. "
            "It doesn't exist on https://bplan-prod.liqd.net/api/".format(
                bplan.identifier, bplan
            )
        )

    bplan.topics = ["URB"]
    bplan.save(update_fields=["point", "administrative_district", "topics"])
