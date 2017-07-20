from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.views import generic

from adhocracy4.follows.models import Follow
from adhocracy4.projects.models import Project
from apps.newsletters.models import ORGANISATION
from apps.newsletters.models import PLATFORM
from apps.newsletters.models import PROJECT
from apps.organisations.models import Organisation
from apps.users.models import User

from . import emails
from . import forms
from . import models


class NewsletterCreateView(generic.CreateView):
    model = models.Newsletter
    form_class = forms.NewsletterForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('meinberlin_newsletters:newsletter-create')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.save()
        form.save_m2m()

        if 'send' in form.data:
            instance.sent = timezone.now()
            instance.save()

            receivers = int(form.cleaned_data['receivers'])
            participant_ids = []
            if not(self.request.user.is_superuser or
                    Organisation.objects.get(
                    pk=int(form.data['organisation'])).
                    has_initiator(self.request.user)):
                raise PermissionDenied

            if receivers == PROJECT:
                participant_ids = Follow.objects.filter(
                    project=int(form.data['project']),
                    enabled=True
                ).values_list('creator', flat=True)

            elif receivers == ORGANISATION:
                participant_ids = Follow.objects.filter(
                    project__organisation=int(form.data['organisation']),
                    enabled=True
                ).values_list('creator', flat=True).distinct()

            elif receivers == PLATFORM:
                participant_ids = User.objects.all().values_list('pk', flat=True)

            emails.NewsletterEmail.send(self.object,
                                        participant_ids=participant_ids)
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
