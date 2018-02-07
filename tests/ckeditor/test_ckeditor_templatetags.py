import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_transform_collapsibles(project_factory):
    project = project_factory(information='<div class="collapsible-item">'
                              '<div class="collapsible-item-title">Title</div>'
                              '<div class="collapsible-item-body">Body</div>'
                              '</div>')

    template = '{% load ckeditor_tags %}' + \
               '{{ project.information|transform_collapsibles|safe }}'
    output = render_template(template, {'project': project})
    assert '<span>Title</span>' in output
    assert '<div>Body</div>' in output
