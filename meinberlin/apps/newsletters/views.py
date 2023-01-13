from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic

from adhocracy4.dashboard import mixins as a4dashboard_mixins
from adhocracy4.follows.models import Follow
from adhocracy4.rules import mixins as rules_mixins

from . import emails
from . import models
from .forms import NewsletterForm
from .forms import RestrictedNewsletterForm

Organisation = apps.get_model(settings.A4_ORGANISATIONS_MODEL)


class DashboardNewsletterCreateView(
    a4dashboard_mixins.DashboardBaseMixin,
    rules_mixins.PermissionRequiredMixin,
    generic.CreateView,
):
    menu_item = "newsletter"
    model = models.Newsletter
    form_class = NewsletterForm
    permission_required = "a4projects.add_project"

    def get_permission_object(self):
        return self.organisation

    def _check_permission(self, organisation, user):
        return (
            user.is_superuser
            or organisation.has_initiator(user)
            or self._group_permission(organisation, user)
        )

    def _group_permission(self, organisation, user):
        org_groups = organisation.groups.all()
        user_groups = user.groups.all()
        return (org_groups & user_groups).count() > 0

    def get_email_kwargs(self):
        kwargs = {}
        kwargs.update({"organisation_pk": self.organisation.pk})
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["organisation"] = self.organisation

        kwargs["initial"] = {
            "sender_name": self.organisation.name,
            "sender": settings.CONTACT_EMAIL,
        }

        if not self._check_permission(self.organisation, self.request.user):
            kwargs["initial"]["receivers"] = models.PROJECT

        return kwargs

    def get_success_url(self):
        return reverse(
            "a4dashboard:newsletter-create",
            kwargs={"organisation_slug": self.organisation.slug},
        )

    def get_form(self):
        if self._check_permission(self.organisation, self.request.user):
            return NewsletterForm(**self.get_form_kwargs())
        else:
            return RestrictedNewsletterForm(**self.get_form_kwargs())

    def get_template_names(self):
        user = self.request.user
        if self.organisation.has_initiator(user) or user.is_superuser:
            return ["meinberlin_newsletters/newsletter_dashboard_form.html"]
        else:
            return [
                "meinberlin_newsletters/" "restricted_newsletter_dashboard_form.html"
            ]

    def form_valid(self, form):
        # Check if the current user is allowed to send to the selected org
        organisation = form.cleaned_data["organisation"]
        if not self._check_permission(organisation, self.request.user):
            raise PermissionDenied

        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.sent = timezone.now()
        instance.save()
        form.save_m2m()

        receivers = int(form.cleaned_data["receivers"])

        if receivers == models.PROJECT:
            participant_ids = Follow.objects.filter(
                project=form.cleaned_data["project"].pk, enabled=True
            ).values_list("creator", flat=True)

        elif receivers == models.ORGANISATION:
            participant_ids = (
                Follow.objects.filter(
                    project__organisation=organisation.pk, enabled=True
                )
                .values_list("creator", flat=True)
                .distinct()
            )

        elif receivers == models.INITIATOR:
            participant_ids = (
                Organisation.objects.get(pk=organisation.pk)
                .initiators.all()
                .values_list("pk", flat=True)
            )
        else:
            participant_ids = []

        if receivers == models.PLATFORM:
            emails.NewsletterEmailAll.send(instance, **self.get_email_kwargs())

        else:
            emails.NewsletterEmail.send(
                instance,
                participant_ids=list(participant_ids),
                **self.get_email_kwargs()
            )
        messages.success(
            self.request,
            _("Newsletter has been saved and " "will be sent to the recipients."),
        )

        return HttpResponseRedirect(self.get_success_url())
