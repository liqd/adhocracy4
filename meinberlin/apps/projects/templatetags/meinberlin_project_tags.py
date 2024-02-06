from django import template
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum

from adhocracy4.comments.models import Comment
from adhocracy4.polls.models import Vote as Vote
from meinberlin.apps.budgeting.models import Proposal as budget_proposal
from meinberlin.apps.ideas.models import Idea
from meinberlin.apps.kiezkasse.models import Proposal as kiezkasse_proposal
from meinberlin.apps.likes.models import Like
from meinberlin.apps.livequestions.models import LiveQuestion
from meinberlin.apps.mapideas.models import MapIdea

register = template.Library()


@register.filter
def project_url(project):
    if (
        project.project_type == "meinberlin_bplan.Bplan"
        or project.project_type == "meinberlin_extprojects.ExternalProject"
    ):
        return project.externalproject.url
    return project.get_absolute_url()


@register.filter
def is_external(project):
    return (
        project.project_type == "meinberlin_bplan.Bplan"
        or project.project_type == "meinberlin_extprojects.ExternalProject"
    )


@register.simple_tag
def get_num_entries(module):
    """Count all user-generated items."""
    item_count = (
        Idea.objects.filter(module=module).count()
        + MapIdea.objects.filter(module=module).count()
        + budget_proposal.objects.filter(module=module).count()
        + kiezkasse_proposal.objects.filter(module=module).count()
        + Vote.objects.filter(choice__question__poll__module=module).count()
        + LiveQuestion.objects.filter(module=module).count()
        + Like.objects.filter(question__module=module).count()
    )
    comment_filter = (
        Q(idea__module=module)
        | Q(mapidea__module=module)
        | Q(budget_proposal__module=module)
        | Q(kiezkasse_proposal__module=module)
        | Q(topic__module=module)
        | Q(maptopic__module=module)
        | Q(paragraph__chapter__module=module)
        | Q(chapter__module=module)
        | Q(poll__module=module)
    )
    comment_count = (
        Comment.objects.filter(comment_filter)
        .annotate(child_comment_count=Count("child_comments__pk", distinct=True))
        .aggregate(comment_count=Count("pk") + Sum("child_comment_count"))[
            "comment_count"
        ]
    )
    if comment_count is None:
        comment_count = 0
    return item_count + comment_count
