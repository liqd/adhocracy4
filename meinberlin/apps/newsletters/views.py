from django.apps import apps
from django.conf import settings
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.views import generic

from adhocracy4.follows.models import Follow
from adhocracy4.rules import mixins as rules_mixins

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
        instance = form.save(commit=False)

        # Check if the current user is allowed to send to the selected org
        organisation = form.cleaned_data['organisation']
        if not (self.request.user.is_superuser or
                Organisation.objects.get(pk=organisation.pk)
                    .has_initiator(self.request.user)):
            raise PermissionDenied

        instance.creator = self.request.user
        instance.save()
        form.save_m2m()

        if 'send' in form.data:
            instance.sent = timezone.now()
            instance.save()

            receivers = int(form.cleaned_data['receivers'])
            participant_ids = []

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

            emails.NewsletterEmail.send(instance,
                                        participant_ids=list(participant_ids),
                                        **self.get_email_kwargs())

        return HttpResponseRedirect(self.get_success_url())


class NewsletterUpdateView(generic.UpdateView):
    model = models.Newsletter
    form_class = forms.NewsletterForm

    def form_valid(self, form):
        instance = form.save()

        if 'send' in form.data:
            instance.sent = timezone.now()
            instance.save()
            # TODO: send mails

        return HttpResponseRedirect(self.get_success_url())
