import pytest
from dateutil.parser import parse
from django.urls import reverse
from django.utils import timezone
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from freezegun import freeze_time

from adhocracy4.test.helpers import setup_phase
from meinberlin.apps.budgeting import phases
from meinberlin.apps.budgeting.models import Proposal
from tests.votes.test_token_vote_api import add_token_to_session


@pytest.mark.django_db
def test_proposal_list_mixins(apiclient, phase_factory, proposal_factory,
                              category_factory, voting_token_factory,
                              label_factory):
    phase, module, project, proposal = setup_phase(phase_factory,
                                                   proposal_factory,
                                                   phases.RatingPhase)
    category1 = category_factory(module=module)
    category2 = category_factory(module=module)
    token = voting_token_factory(module=module)
    add_token_to_session(apiclient, token)

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})

    response = apiclient.get(url)

    # pagination
    assert 'count' in response.data
    assert response.data['count'] == 1
    assert 'page_count' in response.data
    assert response.data['page_count'] == 1

    # filter info
    assert 'filters' in response.data
    assert len(response.data['filters']) == 3

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

    assert 'ordering' in response.data['filters']
    assert response.data['filters']['ordering']['label'] == _('Ordering')
    assert response.data['filters']['ordering']['choices'] == \
           [('-created', _('Most recent')),
            ('-positive_rating_count', _('Most popular')),
            ('-comment_count', _('Most commented')),
            ('dailyrandom', _('Random'))]
    assert response.data['filters']['ordering']['default'] == 'dailyrandom'

    # locale info
    assert 'locale' in response.data
    assert response.data['locale'] == translation.get_language()

    # token info
    assert 'token_info' in response.data
    assert response.data['token_info']['votes_left']
    assert response.data['token_info']['num_votes_left'] == 5

    # with labels
    label1 = label_factory(module=module)
    label2 = label_factory(module=module)

    response = apiclient.get(url)
    assert 'filters' in response.data
    assert len(response.data['filters']) == 4
    assert 'labels' in response.data['filters']
    assert (str(label1.pk), label1.name) in \
           response.data['filters']['labels']['choices']
    assert (str(label2.pk), label2.name) in \
           response.data['filters']['labels']['choices']


@pytest.mark.django_db
def test_proposal_list_filtering(apiclient, module, proposal_factory,
                                 category_factory, comment_factory,
                                 rating_factory, label_factory):
    category1 = category_factory(module=module)
    category2 = category_factory(module=module)
    label1 = label_factory(module=module)
    label2 = label_factory(module=module)

    now = parse('2022-01-01 18:00:00 UTC')
    yesterday = now - timezone.timedelta(days=1)
    last_week = now - timezone.timedelta(days=7)

    proposal_new = proposal_factory(pk=1, module=module, created=now)
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

    proposal_cat1 = proposal_factory(pk=6,
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

    # queryset is ordered by created
    response = apiclient.get(url)
    assert len(response.data['results']) == 8
    assert response.data['results'][0]['pk'] == proposal_new.pk
    assert response.data['results'][-1]['pk'] == proposal_old.pk

    # archived filter
    querystring = '?is_archived=false'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 6
    querystring = '?is_archived=true'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2
    assert proposal_archived_labels.pk in \
           [p['pk'] for p in response.data['results']]

    # category filter
    querystring = '?category=' + str(category1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_cat1.pk
    querystring = '?category=' + str(category2.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2

    # label filter
    querystring = '?labels=' + str(label1.pk)
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['pk'] == proposal_archived_labels.pk
    assert response.data['results'][1]['pk'] == proposal_popular_labels.pk

    # search filter
    querystring = '?search=liqd+proposal'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_old.pk

    querystring = '?search=2021-'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 7

    querystring = '?search=2022-'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_new.pk

    querystring = '?search=2021-00006'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['pk'] == proposal_cat1.pk

    # ordering
    # positive rating
    querystring = '?ordering=-positive_rating_count'
    url_tmp = url + querystring
    response = apiclient.get(url_tmp)
    assert len(response.data['results']) == 8
    assert response.data['results'][0]['pk'] == proposal_popular_labels.pk
    assert response.data['results'][1]['pk'] == proposal_cat2_popular.pk

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


@pytest.mark.django_db
def test_proposal_list_pagination(apiclient, module, proposal_factory):

    url = reverse('proposals-list',
                  kwargs={'module_pk': module.pk})
    response = apiclient.get(url)
    pagesize = response.data['page_size']

    for i in range(pagesize + 1):
        proposal_factory(module=module)

    response = apiclient.get(url)

    assert response.data['count'] == pagesize + 1
    assert response.data['next'].endswith('?page=2')
    assert not response.data['previous']
    assert response.data['page_count'] == 2
    assert len(response.data['results']) == pagesize

    url_tmp = url + '?page=2'
    response = apiclient.get(url_tmp)
    assert not response.data['next']
    assert response.data['previous'].endswith(url)
    assert len(response.data['results']) == 1

    proposal = Proposal.objects.last()
    proposal.is_archived = True
    proposal.save()

    url_tmp = url + '?is_archived=false'
    response = apiclient.get(url_tmp)
    assert not response.data['next']
    assert not response.data['previous']
    assert response.data['page_count'] == 1
    assert len(response.data['results']) == pagesize
