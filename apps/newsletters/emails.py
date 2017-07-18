from django.contrib import auth

from apps.contrib.emails import Email

User = auth.get_user_model()


class NewsletterEmail(Email):
    def get_languages(self, receiver):
        return ['raw']
    template_name = 'meinberlin_newsletters/emails/newsletter_email'

    def get_receivers(self):
        return User.objects.filter(id__in=self.kwargs['participant_ids'])
