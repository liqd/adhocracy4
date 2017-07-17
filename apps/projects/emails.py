from django.contrib import auth

from apps.contrib.emails import Email

User = auth.get_user_model()


class InviteParticipantEmail(Email):
    template_name = 'meinberlin_projects/emails/invite_participant'

    def get_receivers(self):
        return User.objects.filter(id__in=self.kwargs['participant_ids'])
