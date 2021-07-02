import pytest

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.documents import phases
from meinberlin.test.helpers import assert_template_response


@pytest.mark.django_db
def test_document_detail_view(client, phase_factory, chapter_factory):
    phase, module, project, item = setup_phase(
        phase_factory, chapter_factory, phases.CommentPhase)
    url = project.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_documents/chapter_detail.html')


@pytest.mark.django_db
def test_chapter_detail_view(client, phase_factory, chapter_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, phases.CommentPhase)
    chapter_factory(module=module, weight=0)
    chapter = chapter_factory(module=module, weight=1)
    url = chapter.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_documents/chapter_detail.html')


@pytest.mark.django_db
def test_paragraph_detail_view(client, phase_factory, chapter_factory,
                               paragraph_factory):
    phase, module, project, item = setup_phase(
        phase_factory, chapter_factory, phases.CommentPhase)
    paragraph = paragraph_factory(chapter=item)
    url = paragraph.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'meinberlin_documents/paragraph_detail.html')
