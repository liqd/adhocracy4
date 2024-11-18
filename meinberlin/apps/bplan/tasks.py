import json
import urllib

from celery import shared_task

from meinberlin.apps import logger
from meinberlin.apps.bplan.models import Bplan

"""These tasks are about to become deprecated/can be removed once the switch to diplan has been completed"""


def get_features_from_bplan_api(endpoint):
    url = "https://bplan-prod.liqd.net/api/" + endpoint
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    res_body = res.read()
    res_json = json.loads(res_body.decode("utf-8"))

    return res_json.get("features")


def get_bplan_point(bplan_identifier):
    url_poi = "bplan/points/" + "?bplan={}".format(bplan_identifier.replace(" ", "%20"))

    try:
        features = get_features_from_bplan_api(url_poi)
        if features:
            point = features[0]
            return point

        return None

    except UnicodeEncodeError:
        # catches bplan-identifiers with problematic chars
        return None


@shared_task
def get_location_information(bplan_id: int):
    """Fetch and update the location information for a bplan.
    Called via the post_save signal in signals.py. To prevent the signal
    from retriggering after updating the location information save() needs
    to be called with the update_fields parameter: save(update_fields=["point"]).

    This will become unnecessary with the switch to diplan, as they already send the location to us.

    Parameters
        ----------
        bplan_id
            The primary key of the bplan
    """
    bplan = Bplan.objects.get(pk=bplan_id)
    point = get_bplan_point(bplan.identifier)

    if point:
        bplan.point = point
    else:
        logger.error(
            "The identifier '{}' for bplan '{}' seems to be wrong. "
            "It doesn't exist on https://bplan-prod.liqd.net/api/".format(
                bplan.identifier, bplan
            )
        )
    bplan.save(update_fields=["point"])
