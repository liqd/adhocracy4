from django.db.models import signals
from django.dispatch import receiver

from adhocracy4.actions.models import Action as A4Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.follows.models import Follow
from adhocracy4.projects.models import Project
from apps.actions.models import Action

from . import emails


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
                    creator_id=user,
                    defaults={
                        'enabled': True
                    }
                )
