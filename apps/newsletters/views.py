from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.views import generic

from adhocracy4.follows.models import Follow
from adhocracy4.projects.models import Project
from apps.newsletters.models import PROJECT, PLATFORM, ORGANISATION
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

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.save()
        form.save_m2m()

        if 'send' in form.data:
            instance.sent = timezone.now()
            instance.save()
            # TODO: send mails
            receivers = int(form.cleaned_data['receivers'])
            if receivers == PROJECT:

                project_follower = Follow.objects.filter(
                    project=Project.objects.get(id=form.data['project']),
                    enabled=True)

                participant_ids = [follow.creator.id for follow in project_follower]
                emails.NewsletterEmail.send(self.object,
                                            participant_ids=participant_ids)
            elif receivers == ORGANISATION:
                organisation_followers = Follow.objects.filter(
                    project__organisation=int(form.data['organisation']),
                    enabled=True
                ).values('creator').distinct()
                participant_ids = [follow['creator'] for follow in organisation_followers]
                emails.NewsletterEmail.send(self.object,
                                            participant_ids=participant_ids)
            elif receivers == PLATFORM:
                users = User.objects.all()
                participant_ids = [user.id for user in users]
                emails.NewsletterEmail.send(self.object,
                                            participant_ids=participant_ids)
        return HttpResponseRedirect(reverse(
            'meinberlin_newsletters:newsletter-create'))


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
