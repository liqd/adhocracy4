import pytest

from adhocracy4.test.helpers import assert_template_response
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import freeze_post_phase
from adhocracy4.test.helpers import redirect_target
from meinberlin.apps.bplan import phases
from tests.helpers import get_emails_for_address_and_subject


@pytest.mark.django_db
def test_statement_form_view(client, phase_factory, bplan_factory, module_factory):
    bplan = bplan_factory(is_draft=False)
    module = module_factory(project=bplan)
    phase = phase_factory(phase_content=phases.StatementPhase(), module=module)
    url = bplan.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, "meinberlin_bplan/statement_create_form.html"
        )

        statement = {
            "name": "User",
            "email": "user@foo.bar",
            "street_number": "Some Street 1",
            "postal_code_city": "12345 City",
            "statement": "Something...",
        }
        response = client.post(url, statement)
        assert redirect_target(response) == "statement-sent"


@pytest.mark.django_db
def test_statement_emails(client, phase_factory, bplan_factory, module_factory):
    bplan = bplan_factory(is_draft=False)
    module = module_factory(project=bplan)
    phase = phase_factory(phase_content=phases.StatementPhase(), module=module)
    url = bplan.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, "meinberlin_bplan/statement_create_form.html"
        )

        statement = {
            "name": "User",
            "email": "user@foo.bar",
            "street_number": "Some Street 1",
            "postal_code_city": "12345 City",
            "statement": "Paragraph 1" "",
        }
        response = client.post(url, statement)
        assert redirect_target(response) == "statement-sent"
        office_worker_emails = get_emails_for_address_and_subject(
            bplan.office_worker_email, "Neue Stellungnahme zu"
        )
        user_emails = get_emails_for_address_and_subject(
            "user@foo.bar", "Ihre Stellungnahme zum"
        )
        assert len(office_worker_emails) == 1
        assert len(user_emails) == 1
        assert "<p>Paragraph 1</p>" in office_worker_emails[0].body
        assert "<p>Paragraph 1</p>" in user_emails[0].body


@pytest.mark.django_db
def test_statement_form_view_post_phase(
    client, phase_factory, bplan_factory, module_factory
):
    bplan = bplan_factory(is_draft=False)
    module = module_factory(project=bplan)
    phase = phase_factory(phase_content=phases.StatementPhase(), module=module)
    url = bplan.get_absolute_url()
    with freeze_post_phase(phase):
        response = client.get(url)
        assert response.status_code == 302
        assert redirect_target(response) == "finished"
