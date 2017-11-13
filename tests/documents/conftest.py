from pytest_factoryboy import register

from meinberlin.apps.test.factories import documents as document_factories

register(document_factories.ChapterFactory)
register(document_factories.ParagraphFactory)
