import pytest
from dateutil.parser import parse
from django.urls import reverse
from freezegun import freeze_time


@pytest.mark.django_db
def test_modules(client, project, module_factory, phase_factory):
    module1 = module_factory(project=project, weight=1)
    module2 = module_factory(project=project, weight=2)
    module3 = module_factory(project=project, weight=3)
    module4 = module_factory(project=project, weight=4)
    phase_factory(
        module=module1,
        start_date=parse("2013-01-01 17:10:00 UTC"),
        end_date=parse("2013-01-01 18:05:00 UTC"),
    )
    phase_factory(
        module=module1,
        start_date=parse("2013-01-02 19:00:00 UTC"),
        end_date=parse("2013-01-02 19:05:00 UTC"),
    )
    phase_factory(
        module=module2,
        start_date=parse("2013-01-01 17:05:00 UTC"),
        end_date=parse("2013-01-01 19:00:00 UTC"),
    )
    phase_factory(
        module=module3,
        start_date=parse("2013-01-01 17:00:00 UTC"),
        end_date=parse("2013-01-01 18:05:00 UTC"),
    )
    phase_factory(
        module=module4,
        start_date=parse("2013-01-01 19:05:00 UTC"),
        end_date=parse("2013-01-01 20:00:00 UTC"),
    )

    url = reverse("project-detail", kwargs={"slug": project.slug})
    response = client.get(url)
    with freeze_time(parse("2013-01-01 18:00:00 UTC")):
        assert module1 in response.context_data["modules"]
        assert module2 in response.context_data["modules"]
        assert module3 == response.context_data["modules"][0]
        assert module4 in response.context_data["modules"]
