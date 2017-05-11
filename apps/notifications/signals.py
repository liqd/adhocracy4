from django.db.models import signals
from django.dispatch import receiver

from adhocracy4.actions.models import Action
from adhocracy4.actions.verbs import Verbs
from adhocracy4.follows.models import Follow
from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project
from apps.organisations.models import Organisation
from . import emails


@receiver(signals.post_save, sender=Action)
def send_notifications(instance, created, **kwargs):
    action = instance
    verb = Verbs(action.verb)

    if verb == Verbs.CREATE or verb == Verbs.ADD:
        emails.NotifyCreatorEmail.send(action)

        # Try to get the project
        # if action.project:
        #     project = action.project
        # elif action.target:
        #     project = getattr('project', action.target, None)
        # else:
        #     project = None

        if action.project:
            emails.NotifyModeratorsEmail.send(action)
            emails.NotifyFollowersOnNewItemCreated.send(action)

    elif verb == Verbs.SCHEDULE:
        if isinstance(action.obj, Phase):
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


@receiver(signals.m2m_changed, sender=Organisation.initiators.through)
def autofollow_organisation_initiators(instance, action, pk_set, reverse,
                                       **kwargs):
    if action == 'post_add':
        if not reverse:
            organisation = instance
            users_pks = pk_set

            for project in Project.objects.filter(organisation=organisation):
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
            organisation_pk_set = pk_set

            for project in Project.objects.filter(
                    organisation_id__in=organisation_pk_set):
                Follow.objects.update_or_create(
                    project=project,
                    creator=user,
                    defaults={
                        'enabled': True
                    }
                )


@receiver(signals.post_save)
def autofollow_organisation_initiators_new_projects(sender, instance, created,
                                                    **kwargs):
    if issubclass(sender, Project):
        # we have to check if the senders inherits from Project to catch
        # signals from external projects and bplans
        project = instance
        if created:
            for user in project.organisation.initiators.all():
                Follow.objects.update_or_create(
                    project=project,
                    creator=user,
                    defaults={
                        'enabled': True
                    }
                )
