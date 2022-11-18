import pytest
from django.urls import reverse

from adhocracy4.test.helpers import assert_template_response


@pytest.mark.django_db
def test_idea_admin_form(client, user_factory, idea, category_factory,
                         label_factory, module_factory):
    admin = user_factory(is_superuser=True, is_staff=True)
    module = idea.module
    project = module.project
    other_module = module_factory(project=project)

    category = category_factory(module=module)
    category_other_module = category_factory(module=other_module)

    label = label_factory(module=module)
    label_other_module = label_factory(module=other_module)

    client.force_login(admin)

    url = reverse('admin:meinberlin_ideas_idea_change', args=(idea.pk,))
    response = client.get(url)
    assert_template_response(
        response,
        'admin/meinberlin_ideas/idea/change_form.html')
    form = response.context_data['adminform'].form
    assert category in form.fields['category'].queryset
    assert category_other_module not in form.fields['category'].queryset

    assert label in form.fields['labels'].queryset
    assert label_other_module not in form.fields['labels'].queryset
