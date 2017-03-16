from django.contrib.auth import get_user_model
from django.core import urlresolvers

from adhocracy4 import emails

User = get_user_model()


class ReportModeratorEmail(emails.ModeratorNotification):
    template_name = 'report_moderators'


class ReportCreatorEmail(emails.Email):
    template_name = 'report_creator'

    def get_receivers(self):
        return [self.object.content_object.creator]
