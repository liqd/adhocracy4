from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from adhocracy4.rules import mixins as rules_mixins

from . import emails
from . import forms


class InitiatorRequestView(rules_mixins.PermissionRequiredMixin,
                           FormView):

    template_name = 'meinberlin_initiators/request.html'
    permission_required = 'meinberlin_initiators.request'
    form_class = forms.InitiatorRequestForm
    success_url = '/'

    def form_valid(self, form):
        organisation = form.cleaned_data['organisation']
        emails.InitiatorRequest.send(self.request.user,
                                     phone=form.cleaned_data['phone'],
                                     organisation_id=organisation.id)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Request was send.'))
        return super().form_valid(form)
