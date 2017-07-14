from django.http.response import HttpResponseRedirect
from django.utils import timezone
from django.views import generic

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
