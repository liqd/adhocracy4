from django import template

from adhocracy4.comments.models import Comment
from meinberlin.apps.budgeting.models import Proposal as budget_proposal
from meinberlin.apps.ideas.models import Idea
from meinberlin.apps.kiezkasse.models import Proposal as kiezkasse_proposal
from meinberlin.apps.likes.models import Like
from meinberlin.apps.livequestions.models import LiveQuestion
from meinberlin.apps.mapideas.models import MapIdea
from meinberlin.apps.polls.models import Vote

register = template.Library()


@register.filter
def project_url(project):
    if (project.project_type == 'meinberlin_bplan.Bplan'
            or project.project_type ==
            'meinberlin_extprojects.ExternalProject'):
        return project.externalproject.url
    return project.get_absolute_url()


@register.filter
def is_external(project):
    return (project.project_type == 'meinberlin_bplan.Bplan'
            or project.project_type ==
            'meinberlin_extprojects.ExternalProject')


@register.simple_tag
def get_num_entries(module):
    """Count all user-generated items."""
    item_count = \
        Idea.objects.filter(module=module).count() \
        + MapIdea.objects.filter(module=module).count() \
        + budget_proposal.objects.filter(module=module).count() \
        + kiezkasse_proposal.objects.filter(module=module).count() \
        + Comment.objects.filter(idea__module=module).count() \
        + Comment.objects.filter(mapidea__module=module).count() \
        + Comment.objects.filter(budget_proposal__module=module).count() \
        + Comment.objects.filter(kiezkasse_proposal__module=module).count() \
        + Comment.objects.filter(topic__module=module).count() \
        + Comment.objects.filter(maptopic__module=module).count() \
        + Comment.objects.filter(paragraph__chapter__module=module).count() \
        + Comment.objects.filter(chapter__module=module).count() \
        + Comment.objects.filter(poll__module=module).count() \
        + Vote.objects.filter(choice__question__poll__module=module).count() \
        + LiveQuestion.objects.filter(module=module).count() \
        + Like.objects.filter(question__module=module).count()
    return item_count
