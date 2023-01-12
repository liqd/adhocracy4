import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_absolute_url(proposal):
    url = reverse('meinberlin_budgeting:proposal-detail',
                  kwargs={'pk': '{:05d}'.format(proposal.pk),
                          'year': proposal.created.year})
    assert proposal.get_absolute_url() == url


@pytest.mark.django_db
def test_str(proposal):
    proposal_string = proposal.__str__()
    assert proposal_string == proposal.name


@pytest.mark.django_db
def test_project(proposal):
    assert proposal.module.project == proposal.project


@pytest.mark.django_db
def test_proposal_badges_properties(
        proposal_factory, category, label_factory):
    module = category.module
    proposal = proposal_factory(
        module=module,
        moderator_status='CHECKED',
        category=category,
        budget=40,
        point_label='somewhere'
    )
    label_1 = label_factory(module=module)
    label_2 = label_factory(module=module)
    label_3 = label_factory(module=module)
    proposal.labels.set([label_1, label_2, label_3])

    assert proposal.item_badges == \
        [['moderator_status',
          proposal.get_moderator_status_display(),
          proposal.moderator_status],
         ['budget', '{}€'.format(proposal.budget)],
         ['point_label', proposal.point_label],
         ['category', category.name],
         ['label', label_1.name],
         ['label', label_2.name],
         ['label', label_3.name]]
    assert proposal.item_badges_for_list == \
        [['moderator_status',
          proposal.get_moderator_status_display(),
          proposal.moderator_status],
         ['budget', '{}€'.format(proposal.budget)],
         ['point_label', proposal.point_label]]
    assert proposal.additional_item_badges_for_list_count == 4
