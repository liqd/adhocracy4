from django.conf import settings


def get_map_settings(**kwargs):
    map_settings = {
        "mapboxToken": "",
        "omtToken": "",
        "attribution": "",
        "useVectorMap": 0,
        "baseUrl": settings.A4_MAP_BASEURL,
        **kwargs,
    }

    if hasattr(settings, "A4_MAP_ATTRIBUTION"):
        map_settings["attribution"] = settings.A4_MAP_ATTRIBUTION

    if hasattr(settings, "A4_USE_VECTORMAP") and settings.A4_USE_VECTORMAP:
        map_settings["useVectorMap"] = 1

    if hasattr(settings, "A4_MAPBOX_TOKEN"):
        map_settings["mapboxToken"] = settings.A4_MAPBOX_TOKEN

    if hasattr(settings, "A4_OPENMAPTILES_TOKEN"):
        map_settings["omtToken"] = settings.A4_OPENMAPTILES_TOKEN

    # Filter out the keys that have a value of ""
    return {key: val for key, val in map_settings.items() if val != ""}
