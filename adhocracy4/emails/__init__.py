from .base import get_email_base


class ExternalNotification(get_email_base()):
    email_attr_name = "email"

    def get_receivers(self):
        return [getattr(self.object, self.email_attr_name)]


class UserNotification(get_email_base()):
    user_attr_name = "creator"

    def get_receivers(self):
        return [getattr(self.object, self.user_attr_name)]


class ModeratorNotification(get_email_base()):
    def get_receivers(self):
        return self.object.project.moderators.all()


class InitiatorNotification(get_email_base()):
    def get_receivers(self):
        return self.object.organisation.initiators.all()
