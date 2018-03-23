from django.conf import settings

from meinberlin.apps.contrib.emails import Email


class OfficeWorkerNotification(Email):
    template_name = 'meinberlin_bplan/emails/office_worker_notification'

    @property
    def office_worker_email(self):
        project = self.object.module.project
        return project.externalproject.bplan.office_worker_email

    def get_receivers(self):
        return [self.office_worker_email]

    def get_context(self):
        context = super().get_context()
        context['module'] = self.object.module
        context['project'] = self.object.module.project
        context['contact_email'] = settings.CONTACT_EMAIL
        return context


class SubmitterConfirmation(Email):
    template_name = 'meinberlin_bplan/emails/submitter_confirmation'

    def get_receivers(self):
        return [self.object.email]

    def get_context(self):
        context = super().get_context()
        context['module'] = self.object.module
        context['project'] = self.object.module.project
        context['contact_email'] = settings.CONTACT_EMAIL
        return context
