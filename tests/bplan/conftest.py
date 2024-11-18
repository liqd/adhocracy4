import pytest
from django.core.management import CommandError
from django.core.management import call_command
from pytest_factoryboy import register

from meinberlin.test.factories import bplan as bplan_factories

register(bplan_factories.BplanFactory)


@pytest.fixture
def districts(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # pytest / make pytest
        try:
            call_command(
                "loaddata", "meinberlin/fixtures/administrative_districts.json"
            )
            return
        except CommandError:
            pass
        # when running tests individually from ide (e.g. pycharm)
        try:
            call_command(
                "loaddata", "../../meinberlin/fixtures/administrative_districts.json"
            )
            return
        except CommandError:
            pass
        print("warning: failed to load district fixture")
