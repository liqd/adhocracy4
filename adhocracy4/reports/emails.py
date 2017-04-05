from django.contrib.auth import get_user_model

from adhocracy4 import emails

User = get_user_model()


class ReportModeratorEmail(emails.ModeratorNotification):
    template_name = 'a4reports/emails/report_moderators'


class ReportCreatorEmail(emails.Email):
    template_name = 'a4reports/emails/report_creator'

    def get_receivers(self):
        return [self.object.content_object.creator]
