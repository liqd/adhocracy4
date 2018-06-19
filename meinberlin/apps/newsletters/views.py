from django.apps import apps
from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.dashboard import mixins as a4dashboard_mixins
from adhocracy4.follows.models import Follow
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.newsletters.forms import NewsletterForm

from . import emails
from . import forms
from . import models

Organisation = apps.get_model(settings.A4_ORGANISATIONS_MODEL)
User = auth.get_user_model()


class NewsletterCreateView(rules_mixins.PermissionRequiredMixin,
                           generic.CreateView):
    model = models.Newsletter
    form_class = forms.NewsletterForm
    permission_required = 'is_superuser'

    def get_email_kwargs(self):
        kwargs = {}
        kwargs.update({'organisation_pk': None})
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        if hasattr(self, 'organisation'):
            sender_name = self.organisation.name
        else:
            sender_name = settings.WAGTAIL_SITE_NAME

        kwargs['initial'] = {
            'sender_name': sender_name,
            'sender': settings.CONTACT_EMAIL
        }
        return kwargs

    def get_success_url(self):
        return reverse('meinberlin_newsletters:newsletter-create')

    def form_valid(self, form):
        # Check if the current user is allowed to send to the selected org
        organisation = form.cleaned_data['organisation']
        if not (self.request.user.is_superuser or
                Organisation.objects.get(pk=organisation.pk)
                    .has_initiator(self.request.user)):
            raise PermissionDenied

        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.sent = timezone.now()
        instance.save()
        form.save_m2m()

        receivers = int(form.cleaned_data['receivers'])

        if receivers == models.PROJECT:
            participant_ids = Follow.objects.filter(
                project=form.cleaned_data['project'].pk,
                enabled=True
            ).values_list('creator', flat=True)

        elif receivers == models.ORGANISATION:
            participant_ids = Follow.objects.filter(
                project__organisation=organisation.pk,
                enabled=True
            ).values_list('creator', flat=True).distinct()

        elif receivers == models.PLATFORM:
            participant_ids = User.objects.all().values_list('pk',
                                                             flat=True)

        elif receivers == models.INITIATOR:
            participant_ids = Organisation.objects.get(
                pk=organisation.pk).initiators.all()\
                .values_list('pk', flat=True)
        else:
            participant_ids = []

        if receivers == models.PLATFORM:
            emails.NewsletterEmailAll.send(instance,
                                           **self.get_email_kwargs())

        else:
            emails.NewsletterEmail.send(instance,
                                        participant_ids=list(participant_ids),
                                        **self.get_email_kwargs())
        messages.success(self.request,
                         _('Newsletter has been saved and '
                           'will be sent to the recipients.'))

        return HttpResponseRedirect(self.get_success_url())


class DashboardNewsletterCreateView(a4dashboard_mixins.DashboardBaseMixin,
                                    NewsletterCreateView):
    template_name = 'meinberlin_newsletters/newsletter_dashboard_form.html'
    menu_item = 'newsletter'
    form_class = NewsletterForm
    permission_required = 'a4projects.add_project'

    def get_email_kwargs(self):
        kwargs = {}
        kwargs.update({'organisation_pk': self.organisation.pk})
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organisation'] = self.organisation
        kwargs.pop('user')
        return kwargs

    def get_success_url(self):
        return reverse(
            'a4dashboard:newsletter-create',
            kwargs={'organisation_slug': self.organisation.slug})

    def get_permission_object(self):
        return self.organisation
