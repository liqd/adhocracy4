from django import template

from adhocracy4.comments.models import Comment
from meinberlin.apps.budgeting.models import Proposal as budget_proposal
from meinberlin.apps.ideas.models import Idea
from meinberlin.apps.kiezkasse.models import Proposal as kiezkasse_proposal
from meinberlin.apps.mapideas.models import MapIdea
from meinberlin.apps.projects import get_project_type

register = template.Library()


@register.filter
def project_url(project):
    if get_project_type(project) in ('external', 'bplan'):
        return project.externalproject.url
    return project.get_absolute_url()


@register.filter
def project_type(project):
    return get_project_type(project)


@register.filter
def is_external(project):
    return get_project_type(project) in ('external', 'bplan')


@register.filter
def is_container(project):
    return get_project_type(project) == 'container'


@register.simple_tag
def to_class_name(value):
    return value.__class__.__name__


@register.simple_tag
def get_num_entries(module):
    """Count all user-generated items."""
    item_count = Idea.objects.filter(module=module).count() \
        + MapIdea.objects.filter(module=module).count() \
        + budget_proposal.objects.filter(module=module).count() \
        + kiezkasse_proposal.objects.filter(module=module).count() \
        + Comment.objects.filter(idea__module=module).count() \
        + Comment.objects.filter(mapidea__module=module).count() \
        + Comment.objects.filter(budget_proposal__module=module).count() \
        + Comment.objects.filter(kiezkasse_proposal__module=module).count()
    return item_count
