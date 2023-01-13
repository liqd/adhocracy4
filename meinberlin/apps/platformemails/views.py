from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic

from adhocracy4.rules import mixins as rules_mixins

from . import emails
from .forms import PlatformEmailForm
from .models import PlatformEmail

User = auth.get_user_model()


class PlatformEmailCreateView(rules_mixins.PermissionRequiredMixin, generic.CreateView):
    model = PlatformEmail
    form_class = PlatformEmailForm
    permission_required = "is_superuser"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        sender_name = settings.WAGTAIL_SITE_NAME

        kwargs["initial"] = {
            "sender_name": sender_name,
            "sender": settings.CONTACT_EMAIL,
        }
        return kwargs

    def form_valid(self, form):

        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.sent = timezone.now()
        instance.save()
        form.save_m2m()

        emails.PlatformEmail.send(instance)

        messages.success(
            self.request,
            _("Platform email has been saved and " "will be sent to the recipients."),
        )

        return HttpResponseRedirect(reverse("meinberlin_platformemails:create"))
