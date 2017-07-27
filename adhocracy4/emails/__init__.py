from . import base
from . import mixins


class Email(mixins.PlatformEmailMixin, base.EmailBase):
    pass


class ExternalNotification(Email):
    email_attr_name = 'email'

    def get_receivers(self):
        return [getattr(self.object, self.email_attr_name)]


class UserNotification(Email):
    user_attr_name = 'creator'

    def get_receivers(self):
        return [getattr(self.object, self.user_attr_name)]


class ModeratorNotification(Email):
    def get_receivers(self):
        return self.object.project.moderators.all()


class InitiatorNotification(Email):
    def get_receivers(self):
        return self.object.organisation.initiators.all()
