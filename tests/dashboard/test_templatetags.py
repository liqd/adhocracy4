import pytest

from adhocracy4.test.helpers import render_template


@pytest.mark.django_db
def test_get_phase_name(phase):
    template = '{% load a4dashboard_tags %}' \
               '{% get_phase_name type as x %}{{x}}'

    assert 'Asking Phase' == render_template(template, {'type': phase.type})


@pytest.mark.parametrize('value, expected', [(0., '0'),
                                             (50., '50'),
                                             (100., '100'),
                                             (0.5, '0'),
                                             (3.141592, '3')])
def test_percentage(value, expected):
    template = '{% load a4dashboard_tags %}{{ value|percentage:100 }}'
    assert expected == render_template(template, {'value': value})
