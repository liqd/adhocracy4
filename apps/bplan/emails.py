from adhocracy4.emails import Email


class OfficeWorkerNotification(Email):
    template_name = 'meinberlin_bplan/emails/office_worker_notification'

    @property
    def office_worker_email(self):
        project = self.object.project
        return project.externalproject.bplan.office_worker_email

    def get_receivers(self):
        return [self.office_worker_email]

    def get_context(self):
        context = super().get_context()
        context['project'] = self.object.project
        return context


class SubmitterConfirmation(Email):
    template_name = 'meinberlin_bplan/emails/submitter_confirmation'
    fallback_language = 'de'

    def get_receivers(self):
        return [self.object.email]

    def get_context(self):
        context = super().get_context()
        context['project'] = self.object.project
        return context
