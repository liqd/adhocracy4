from unittest.mock import patch

import pytest
import requests
from django.core.exceptions import ValidationError
from django.test import override_settings

from adhocracy4.captcha.fields import CapCaptchaField
from adhocracy4.captcha.verification import verify_cap_token
from adhocracy4.captcha.widgets import CapCaptchaWidget


@override_settings(
    A4_CAP_CAPTCHA_ENDPOINT="http://localhost:3000/sitekey/",
    A4_CAP_CAPTCHA_WIDGET_URL="http://localhost:3000/assets/widget.js",
)
def test_widget_renders_cap_widget():
    html = CapCaptchaWidget().render("captcha", "", attrs={"id": "id_captcha"})

    assert 'data-cap-api-endpoint="http://localhost:3000/sitekey/"' in html
    assert 'data-cap-hidden-field-name="captcha"' in html
    assert "<noscript>" in html


@override_settings(
    A4_CAP_CAPTCHA_WIDGET_URL="http://localhost:3000/assets/widget.js",
)
def test_widget_media_contains_widget_and_helper():
    media = str(CapCaptchaWidget().media)

    assert "a4captcha/cap_captcha.js" in media
    assert "http://localhost:3000/assets/widget.js" in media


@override_settings(CAPTCHA_TEST_ACCEPTED_ANSWER="testpass")
def test_field_accepts_test_answer():
    assert CapCaptchaField().clean("testpass") == "testpass"


@override_settings(CAPTCHA_TEST_ACCEPTED_ANSWER="other")
def test_field_rejects_wrong_test_answer():
    with pytest.raises(ValidationError):
        CapCaptchaField().clean("testpass")


@override_settings(
    A4_CAP_CAPTCHA_ENDPOINT="https://cap.example.com/sitekey/",
    A4_CAP_CAPTCHA_SECRET="secret",
    A4_CAPTCHA_TIMEOUT=3,
    CAPTCHA_TEST_ACCEPTED_ANSWER=None,
)
@patch("adhocracy4.captcha.verification.requests.post")
def test_verify_valid_token(mock_post):
    mock_post.return_value.json.return_value = {"success": True}

    assert verify_cap_token("token") is True
    mock_post.assert_called_once_with(
        "https://cap.example.com/sitekey/siteverify",
        json={"secret": "secret", "response": "token"},
        timeout=3,
    )


@override_settings(
    A4_CAP_CAPTCHA_ENDPOINT="https://cap.example.com/sitekey/",
    A4_CAP_CAPTCHA_SECRET="secret",
    CAPTCHA_TEST_ACCEPTED_ANSWER=None,
)
@patch("adhocracy4.captcha.verification.requests.post")
def test_verify_rejected_token(mock_post):
    mock_post.return_value.json.return_value = {"success": False}

    assert verify_cap_token("token") is False


@override_settings(
    A4_CAP_CAPTCHA_ENDPOINT="https://cap.example.com/sitekey/",
    A4_CAP_CAPTCHA_SECRET="secret",
    CAPTCHA_TEST_ACCEPTED_ANSWER=None,
)
@patch("adhocracy4.captcha.verification.requests.post")
def test_verify_rejects_non_boolean_success(mock_post):
    mock_post.return_value.json.return_value = {"success": "true"}

    assert verify_cap_token("token") is False


@override_settings(
    A4_CAP_CAPTCHA_ENDPOINT="https://cap.example.com/sitekey/",
    A4_CAP_CAPTCHA_SECRET="secret",
    CAPTCHA_TEST_ACCEPTED_ANSWER=None,
)
@patch("adhocracy4.captcha.verification.requests.post")
def test_verify_rejects_malformed_response(mock_post):
    mock_post.return_value.json.return_value = None

    assert verify_cap_token("token") is False


@override_settings(
    A4_CAP_CAPTCHA_ENDPOINT="https://cap.example.com/sitekey/",
    A4_CAP_CAPTCHA_SECRET="secret",
    CAPTCHA_TEST_ACCEPTED_ANSWER=None,
)
@patch(
    "adhocracy4.captcha.verification.requests.post",
    side_effect=requests.RequestException,
)
def test_verify_fails_closed_when_service_is_unreachable(mock_post):
    assert verify_cap_token("token") is False
