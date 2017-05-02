from pytest_factoryboy import register

from tests.documents import factories as document_factories


register(document_factories.DocumentFactory)
register(document_factories.ParagraphFactory)
