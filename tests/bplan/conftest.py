from pytest_factoryboy import register

from meinberlin.apps.test.factories import bplan as bplan_factories

register(bplan_factories.BplanFactory)
