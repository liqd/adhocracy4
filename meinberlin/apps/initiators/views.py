from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from adhocracy4.rules import mixins as rules_mixins

from . import emails
from . import forms


class InitiatorRequestView(rules_mixins.PermissionRequiredMixin,
                           FormView):

    template_name = 'meinberlin_initiators/request.html'
    permission_required = 'is_authenticated'
    form_class = forms.InitiatorRequestForm
    success_url = '/'

    def form_valid(self, form):
        emails.InitiatorRequest.send(self.request.user, **form.cleaned_data)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Request was send.'))
        return super().form_valid(form)
