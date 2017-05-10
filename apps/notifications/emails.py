from django.contrib import auth

from adhocracy4 import emails

User = auth.get_user_model()


def _filter_actor_disabled(receivers, actor):
    # TODO: filter if actor has disabled notfications
    return [receiver for receiver in receivers if not receiver == actor]


class NotifyCreatorEmail(emails.Email):
    template_name = 'meinberlin_notifications/emails/notify_creator'

    def get_receivers(self):
        action = self.object
        if hasattr(action.target, 'creator'):
            return _filter_actor_disabled([action.target.creator],
                                          action.actor)
        return []


class NotifyModeratorsEmail(emails.ModeratorNotification):
    template_name = 'meinberlin_notifications/emails/notify_moderator'

    def get_receivers(self):
        action = self.object
        return _filter_actor_disabled(super().get_receivers(), action.actor)


class NotifyFollowersOnPhaseIsOverSoonEmail(emails.Email):
    template_name = 'meinberlin_notifications/emails' \
                    '/notify_followers_over_soon'

    def get_receivers(self):
        action = self.object
        return User.objects.filter(
            follow__project=action.project,
            follow__enabled=True,
            # get_notifications=True
        )


class NotifyFollowersOnNewItemCreated(emails.Email):
    template_name = 'meinberlin_notifications/emails/notify_followers_new_item'

    def get_receivers(self):
        action = self.object
        moderator_ids = action.project.moderators.values_list('id', flat=True)
        return User.objects.filter(
            follow__project=action.project,
            follow__enabled=True,
            # get_notifications=True,
        ).exclude(
            id__in=moderator_ids
        )
