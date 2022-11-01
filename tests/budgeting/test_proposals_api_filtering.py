import pytest
from dateutil.parser import parse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from freezegun import freeze_time

from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases


@pytest.mark.django_db
def test_proposal_list_mixins(apiclient, phase_factory, proposal_factory,
                              category_factory, label_factory):
    phase, module, project, proposal = setup_phase(phase_factory,
                                                   proposal_factory,
                                                   phases.SupportPhase)
    category1 = category_factory(module=module)
    category2 = category_factory(module=module)

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    response = apiclient.get(url)

    # filter info
    assert 'filters' in response.data
    assert len(response.data['filters']) == 4

    assert 'category' in response.data['filters']
    assert response.data['filters']['category']['label'] == _('Category')
    assert response.data['filters']['category']['choices'][0] == ('', _('All'))
    assert (str(category1.pk), category1.name) in \
           response.data['filters']['category']['choices']
    assert (str(category2.pk), category2.name) in \
           response.data['filters']['category']['choices']

    assert 'is_archived' in response.data['filters']
    assert response.data['filters']['is_archived']['label'] == _('Archived')
    assert response.data['filters']['is_archived']['choices'] == \
           [('', _('All')), ('false', _('No')), ('true', _('Yes'))]
    assert response.data['filters']['is_archived']['default'] == 'false'

    assert 'moderator_feedback' in response.data['filters']
    assert response.data['filters']['moderator_feedback']['label'] == \
        _('Status')
    assert response.data['filters']['moderator_feedback']['choices'] == \
           [('', _('All')),
            ('CONSIDERATION', _('Under consideration')),
            ('CHECKED', _('Checked')),
            ('REJECTED', _('Rejected')),
            ('ACCEPTED', _('Accepted'))]

    assert 'ordering' in response.data['filters']
    assert response.data['filters']['ordering']['label'] == _('Ordering')
    assert response.data['filters']['ordering']['choices'] == \
           [('-created', _('Most recent')),
            ('-comment_count', _('Most commented')),
            ('dailyrandom', _('Random'))]
    assert response.data['filters']['ordering']['default'] == 'dailyrandom'

    # with labels
    label1 = label_factory(module=module)
    label2 = label_factory(module=module)

    response = apiclient.get(url)
    assert 'filters' in response.data
    assert len(response.data['filters']) == 5
    assert 'labels' in response.data['filters']
    assert (str(label1.pk), label1.name) in \
           response.data['filters']['labels']['choices']
    assert (str(label2.pk), label2.name) in \
           response.data['filters']['labels']['choices']

    with freeze_phase(phase):
        response = apiclient.get(url)
        assert response.data['filters']['ordering']['choices'] == \
               [('-created', _('Most recent')),
                ('-positive_rating_count', _('Most support')),
                ('-comment_count', _('Most commented')),
                ('dailyrandom', _('Random'))]

    phase_factory(phase_content=phases.RatingPhase(), module=module)
    response = apiclient.get(url)
    assert response.data['filters']['ordering']['choices'] == \
           [('-created', _('Most recent')),
            ('-positive_rating_count', _('Most popular')),
            ('-comment_count', _('Most commented')),
            ('dailyrandom', _('Random'))]


@pytest.mark.django_db
def test_proposal_category_filter(
        apiclient, module, proposal_factory, category_factory):
    category1 = category_factory(module=module)
    category2 = category_factory(module=module)

    proposal_cat1 = proposal_factory(
        module=module, category=category1
    )
    proposal_factory(
        module=module, category=category2
    )
    proposal_factory(
        module=module, category=category2
    )

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    response = apiclient.get(url)
    assert len(response.data['results']) == 3

    querystring = '?category=' + str(category1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_cat1.pk

    querystring = '?category=' + str(category2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2


@pytest.mark.django_db
def test_proposal_label_filter(
        apiclient, module, proposal_factory, label_factory):
    label1 = label_factory(module=module)
    label2 = label_factory(module=module)

    proposal_1 = proposal_factory(module=module)
    proposal_1.labels.set([label1])
    proposal_2 = proposal_factory(module=module)
    proposal_2.labels.set([label1, label2])
    proposal_factory(module=module)

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    response = apiclient.get(url)
    assert len(response.data['results']) == 3

    querystring = '?labels=' + str(label1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2
    assert response.data['results'][1]['pk'] == proposal_1.pk
    assert response.data['results'][0]['pk'] == proposal_2.pk

    querystring = '?labels=' + str(label2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_2.pk


@pytest.mark.django_db
def test_proposal_archived_filter(
        apiclient, module, proposal_factory):

    proposal_archived = proposal_factory(
        module=module, is_archived=True)
    proposal = proposal_factory(module=module)

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    response = apiclient.get(url)
    assert len(response.data['results']) == 2

    # archived filter
    querystring = '?is_archived=false'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal.pk

    querystring = '?is_archived=true'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_archived.pk

    querystring = '?is_archived='
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2


@pytest.mark.django_db
def test_proposal_moderator_feedback_filter(
        apiclient, module, proposal_factory):
    proposal_factory(
        module=module,
        moderator_feedback=''
    )
    proposal_2 = proposal_factory(
        module=module,
        moderator_feedback='CONSIDERATION'
    )
    proposal_3 = proposal_factory(
        module=module,
        moderator_feedback='CHECKED'
    )
    proposal_4 = proposal_factory(
        module=module,
        moderator_feedback='REJECTED'
    )
    proposal_5 = proposal_factory(
        module=module,
        moderator_feedback='ACCEPTED'
    )

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    response = apiclient.get(url)
    assert len(response.data['results']) == 5

    querystring = '?moderator_feedback=CONSIDERATION'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_2.pk

    querystring = '?moderator_feedback=CHECKED'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_3.pk

    querystring = '?moderator_feedback=REJECTED'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_4.pk

    querystring = '?moderator_feedback=ACCEPTED'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_5.pk


@pytest.mark.django_db
def test_proposal_search_filter(
        apiclient, module, proposal_factory):

    now = parse('2022-01-02 18:00:00 UTC')
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)

    proposal_1 = proposal_factory(
        pk=1,
        module=module,
        name='liqd proposal',
        created=now
    )
    proposal_factory(
        pk=2,
        module=module,
        name='other proposal',
        created=last_week
    )
    proposal_factory(
        pk=3,
        module=module,
        name='liqd has good ideas',
        created=yesterday
    )
    proposal_factory(
        pk=4,
        module=module,
        name='idea from 2021',
        created=yesterday
    )
    proposal_5 = proposal_factory(
        pk=5,
        module=module,
        name='blabla',
        created=yesterday
    )

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    response = apiclient.get(url)
    assert len(response.data['results']) == 5

    querystring = '?search=liqd+proposal'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_1.pk

    querystring = '?search=liqd'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2

    querystring = '?search=2021'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2

    querystring = '?search=2021-00'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1

    querystring = '?search=2022-'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 4

    querystring = '?search=2022-00005'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_5.pk

    querystring = '?search='
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 5


@pytest.mark.django_db
def test_proposal_ordering_filter(
        apiclient, module, proposal_factory, comment_factory,
        rating_factory):

    now = parse('2022-01-01 18:00:00 UTC')
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)

    proposal_new = proposal_factory(pk=1, module=module, created=now)
    proposal_old = proposal_factory(pk=2,
                                    module=module,
                                    created=last_week,
                                    name='liqd proposal')

    proposal_factory(pk=3,
                     module=module,
                     created=yesterday,
                     is_archived=True)
    proposal_popular = proposal_factory(pk=4,
                                        module=module,
                                        created=yesterday)
    rating_factory(content_object=proposal_popular)
    rating_factory(content_object=proposal_popular)

    proposal_commented = proposal_factory(pk=5,
                                          module=module,
                                          created=yesterday)
    comment_factory(content_object=proposal_commented)

    proposal_factory(pk=6, module=module, created=yesterday)

    proposal_2_popular = proposal_factory(pk=7,
                                          module=module,
                                          created=yesterday)
    rating_factory(content_object=proposal_2_popular)

    proposal_factory(pk=8,
                     module=module,
                     created=yesterday,
                     is_archived=True)

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    # queryset is ordered by created
    querystring = '?ordering=-created'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 8
    assert response.data['results'][0]['pk'] == proposal_new.pk
    assert response.data['results'][-1]['pk'] == proposal_old.pk

    # positive rating
    querystring = '?ordering=-positive_rating_count'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 8
    assert response.data['results'][0]['pk'] == proposal_popular.pk
    assert response.data['results'][1]['pk'] == proposal_2_popular.pk

    # most commented
    querystring = '?ordering=-comment_count'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 8
    assert response.data['results'][0]['pk'] == proposal_commented.pk

    # daily random
    querystring = '?ordering=dailyrandom'
    url_tmp = url + querystring
    with freeze_time('2020-01-01 00:00:00 UTC'):
        response = apiclient.get(url_tmp)
    ordered_pks = [proposal['pk'] for proposal in response.data['results']]
    assert ordered_pks == [6, 8, 7, 2, 1, 3, 4, 5]
    with freeze_time('2022-01-01 00:00:00 UTC'):
        response = apiclient.get(url_tmp)
    ordered_pks = [proposal['pk'] for proposal in response.data['results']]
    assert ordered_pks == [8, 2, 4, 7, 6, 5, 1, 3]


@pytest.mark.django_db
def test_proposal_filter_combinations(
        apiclient, module, proposal_factory, category_factory,
        comment_factory, rating_factory, label_factory):
    category1 = category_factory(module=module)
    category2 = category_factory(module=module)
    label1 = label_factory(module=module)
    label2 = label_factory(module=module)

    now = parse('2022-01-01 18:00:00 UTC')
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)

    proposal_factory(pk=1, module=module, created=now)
    proposal_old = proposal_factory(pk=2,
                                    module=module,
                                    created=last_week,
                                    name='liqd proposal')

    proposal_archived_labels = proposal_factory(pk=3,
                                                module=module,
                                                created=yesterday,
                                                is_archived=True)
    proposal_archived_labels.labels.set([label1])
    proposal_popular_labels = proposal_factory(pk=4,
                                               module=module,
                                               created=yesterday)
    proposal_popular_labels.labels.set([label1, label2])
    rating_factory(content_object=proposal_popular_labels)
    rating_factory(content_object=proposal_popular_labels)

    proposal_commented = proposal_factory(pk=5,
                                          module=module,
                                          created=yesterday)
    comment_factory(content_object=proposal_commented)

    proposal_factory(pk=6,
                     module=module,
                     created=yesterday,
                     category=category1)

    proposal_cat2_popular = proposal_factory(pk=7,
                                             module=module,
                                             created=yesterday,
                                             category=category2)
    rating_factory(content_object=proposal_cat2_popular)

    proposal_cat2_archived = proposal_factory(pk=8,
                                              module=module,
                                              created=yesterday,
                                              category=category2,
                                              is_archived=True)

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    # combinations
    querystring = '?is_archived=true&category=' + str(category2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_cat2_archived.pk

    querystring = '?is_archived=true&search=2022-'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 0

    querystring = '?ordering=-created&search=2021-'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 7
    assert response.data['results'][6]['pk'] == proposal_old.pk

    querystring = '?ordering=-positive_rating_count&category=' + \
                  str(category2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['pk'] == proposal_cat2_popular.pk
    assert response.data['results'][1]['pk'] == proposal_cat2_archived.pk

    querystring = '?ordering=-positive_rating_count&labels=' + \
                  str(label1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['pk'] == proposal_popular_labels.pk
    assert response.data['results'][1]['pk'] == proposal_archived_labels.pk

    querystring = '?ordering=dailyrandom&category=' + \
                  str(category2.pk)
    url_tmp = url + querystring
    with freeze_time('2020-01-01 00:00:00 UTC'):
        response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['pk'] == proposal_cat2_archived.pk
    assert response.data['results'][1]['pk'] == proposal_cat2_popular.pk
