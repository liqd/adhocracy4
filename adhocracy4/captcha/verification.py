import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def get_captcha_type():
    return getattr(settings, "A4_CAPTCHA_TYPE", "captcheck")


def is_cap_captcha_enabled():
    return bool(
        get_captcha_type() == "cap"
        and getattr(settings, "A4_CAP_CAPTCHA_ENDPOINT", "")
        and getattr(settings, "A4_CAP_CAPTCHA_SECRET", "")
        and getattr(settings, "A4_CAP_CAPTCHA_WIDGET_URL", "")
    )


def verify_cap_token(token):
    """Verify a Cap token with the configured Cap Standalone instance.

    The verification fails closed: missing configuration, an unreachable
    service or an invalid response are all treated as an invalid token.
    """
    if not token:
        return False

    test_answer = getattr(settings, "CAPTCHA_TEST_ACCEPTED_ANSWER", None)
    if test_answer is not None:
        return token == test_answer

    endpoint = getattr(settings, "A4_CAP_CAPTCHA_ENDPOINT", "")
    secret = getattr(settings, "A4_CAP_CAPTCHA_SECRET", "")
    if not endpoint or not secret:
        logger.warning("Cap captcha is not configured.")
        return False

    url = getattr(settings, "A4_CAP_CAPTCHA_SITEVERIFY_URL", "")
    if not url:
        url = endpoint.rstrip("/") + "/siteverify"
    timeout = getattr(settings, "A4_CAPTCHA_TIMEOUT", 5)
    try:
        response = requests.post(
            url,
            json={"secret": secret, "response": token},
            timeout=timeout,
            allow_redirects=False,
        )
        response.raise_for_status()
        payload = response.json()
        success = isinstance(payload, dict) and payload.get("success") is True
    except (requests.RequestException, ValueError, TypeError) as error:
        logger.warning("Cap captcha verification failed: %s", error)
        return False

    if not success:
        logger.warning("Cap captcha token was rejected.")
    return success
