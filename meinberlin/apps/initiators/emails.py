from django.apps import apps
from django.conf import settings

from meinberlin.apps.contrib.emails import Email

Organisation = apps.get_model(settings.A4_ORGANISATIONS_MODEL)


class InitiatorRequest(Email):
    template_name = "meinberlin_initiators/emails/initiator_request"

    def get_receivers(self):
        return [settings.SUPERVISOR_EMAIL]

    def get_context(self):
        context = super().get_context()
        organisation_id = self.kwargs["organisation_id"]
        organisation = Organisation.objects.get(id=organisation_id)
        context["organisation"] = organisation
        return context
