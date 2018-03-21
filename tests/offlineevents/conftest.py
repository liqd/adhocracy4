from pytest_factoryboy import register

from . import factories

register(factories.OfflineEventFactory)
register(factories.OfflineEventDocumentFactory)
