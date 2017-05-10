from django.db.models import signals
from django.dispatch import receiver

from adhocracy4.follows.models import Follow
from adhocracy4.projects.models import Project
from apps.organisations.models import Organisation


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
