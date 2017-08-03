from django.conf import settings

from meinberlin.apps.contrib.emails import Email


class InitiatorRequest(Email):
    template_name = 'meinberlin_initiators/emails/initiator_request'

    def get_receivers(self):
        return [settings.CONTACT_EMAIL]

    def get_context(self):
        context = super().get_context()
        context['organitaion_name'] = self.kwargs.get('organisation_name')
        context['phone'] = self.kwargs.get('phone')
        return context
