from pytest_factoryboy import register

from tests.documents import factories as document_fatories


register(document_fatories.DocumentFactory)
register(document_fatories.ParagraphFactory)
