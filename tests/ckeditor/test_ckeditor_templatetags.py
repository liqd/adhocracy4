import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_transform_collapsibles(project_factory):
    project = project_factory(
        information='<div class="collapsible-item">'
        '<div class="collapsible-item-title">Title</div>'
        '<div class="collapsible-item-body">Body</div>'
        "</div>"
    )

    template = (
        "{% load ckeditor_tags %}"
        + "{{ project.information|transform_collapsibles|safe }}"
    )
    output = render_template(template, {"project": project})
    assert "<span>Title</span>" in output
    assert "<div>Body</div>" in output


@pytest.mark.django_db
def test_disable_iframes(project_factory):
    evil_iframe = (
        '<div><figure class="media"><div '
        'data-oembed-url="https://www.youtube.com/embed/PkhmcJWSNAU'
        '?controls=0"><div><iframe '
        'src="https://www.youtube.com/embed/PkhmcJWSNAU?rel=0"></iframe>'
        "</div></div></figure><p>liqd project info</p></div>"
    )
    good_iframe = (
        '<div><figure class="media"><div '
        'data-oembed-url="https://www.youtube.com/embed/PkhmcJWSNAU'
        '?controls=0"><div><iframe '
        'data-src="https://www.youtube.com/embed/PkhmcJWSNAU?rel=0">'
        "</iframe></div></div></figure><p>liqd project info</p></div>"
    )

    project = project_factory(information=evil_iframe)

    template = (
        "{% load ckeditor_tags %}"
        + "{{ project.information | disable_iframes | safe }}"
    )
    output = render_template(template, {"project": project})
    assert output == good_iframe
