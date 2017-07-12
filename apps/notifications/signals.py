from django.contrib.auth import get_user_model
from django.db.models import signals
from django.dispatch import receiver

from adhocracy4.actions.models import Action as A4Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.follows.models import Follow
from adhocracy4.projects.models import Project
from apps.actions.models import Action

from . import emails

User = get_user_model()


@receiver(signals.post_save, sender=A4Action)
def send_notifications(instance, created, **kwargs):
    action = Action.proxy_of(instance)
    verb = Verbs(action.verb)

    if action.type in ('item', 'comment') \
            and verb in (Verbs.CREATE, Verbs.ADD):
        emails.NotifyCreatorEmail.send(action)

        if action.project:
            emails.NotifyModeratorsEmail.send(action)
            emails.NotifyFollowersOnNewItemCreated.send(action)

    elif action.type == 'phase' and verb == Verbs.SCHEDULE:
        emails.NotifyFollowersOnPhaseIsOverSoonEmail.send(action)


@receiver(signals.m2m_changed, sender=Project.moderators.through)
def autofollow_project_moderators(instance, action, pk_set, reverse, **kwargs):
    if action == 'post_add':
        autofollow_project(instance, pk_set, reverse)


def autofollow_project(instance, pk_set, reverse):
    if not reverse:
        project = instance
        users_pks = pk_set

        for user_pk in users_pks:
            Follow.objects.update_or_create(
                project=project,
                creator_id=user_pk,
                defaults={
                    'enabled': True
                }
            )
    else:
        user = instance
        project_pks = pk_set

        for project_pk in project_pks:
            Follow.objects.update_or_create(
                project_id=project_pk,
                creator=user,
                defaults={
                    'enabled': True
                }
            )


@receiver(signals.m2m_changed, sender=Project.participants.through)
def autofollow_project_participants(instance, action, pk_set, reverse,
                                    **kwargs):
    if action == 'post_add':
        autofollow_project(instance, pk_set, reverse)
    elif action == 'post_remove':
        autounfollow_project_participants_remove(instance, pk_set, reverse)
    elif action == 'post_clear':
        autounfollow_project_participants_clear(instance, reverse)


def autounfollow_project_participants_remove(instance, pk_set, reverse):
    if not reverse:
        for user in User.objects.filter(id__in=pk_set):
            autounfollow_project_participants(instance, user)
    else:
        for project in Project.objects.filter(id__in=pk_set):
            autounfollow_project_participants(project, instance)


def autounfollow_project_participants_clear(instance, reverse):
    if not reverse:
        for follow in Follow.objects.filter(project=instance):
            autounfollow_project_participants(instance, follow.creator)
    else:
        for follow in Follow.objects.filter(creator=instance):
            autounfollow_project_participants(follow.project, instance)


def autounfollow_project_participants(project, user):
    if not user.is_superuser and not project.has_moderator(user):

        Follow.objects \
            .filter(project=project, creator=user) \
            .delete()
