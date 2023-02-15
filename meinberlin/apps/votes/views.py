from django.conf import settings
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django.views import generic

from adhocracy4.dashboard import mixins as dashboard_mixins
from adhocracy4.projects.mixins import ProjectMixin
from meinberlin.apps.votes.forms import TokenBatchCreateForm
from meinberlin.apps.votes.models import TokenPackage
from meinberlin.apps.votes.models import VotingToken
from meinberlin.apps.votes.tasks import PACKAGE_SIZE
from meinberlin.apps.votes.tasks import generate_voting_tokens

TOKENS_PER_MODULE = int(5e6)


class ExportTokenDashboardView(
    ProjectMixin,
    dashboard_mixins.DashboardBaseMixin,
    dashboard_mixins.DashboardComponentMixin,
    generic.TemplateView,
):
    permission_required = "a4projects.change_project"
    template_name = "meinberlin_votes/token_export_dashboard.html"

    def _get_packages(self):
        packages = TokenPackage.objects.filter(module=self.module)
        result = []
        for package in packages:
            if package.is_created:
                result.append((package.pk, package.downloaded, package.num_tokens))
        return result

    def get_permission_object(self):
        return self.project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["token_export_url"] = reverse(
            "a4dashboard:token-export", kwargs={"module_slug": self.module.slug}
        )
        context["number_of_module_tokens"] = intcomma(
            TokenPackage.get_sum_token(self.module)
        )
        context["token_packages"] = self._get_packages()
        context["export_size"] = intcomma(PACKAGE_SIZE)
        context["contact_email"] = settings.CONTACT_EMAIL
        return context


class TokenGenerationDashboardView(
    ProjectMixin,
    dashboard_mixins.DashboardBaseMixin,
    dashboard_mixins.DashboardComponentMixin,
    generic.base.TemplateResponseMixin,
    generic.edit.FormMixin,
    generic.edit.ProcessFormView,
):
    model = VotingToken
    form_class = TokenBatchCreateForm
    success_message = (
        _(
            "{} code will be generated in the background. "
            "This may take a few minutes."
        ),
        _(
            "{} codes will be generated in the background. "
            "This may take a few minutes."
        ),
    )
    error_message_token_number = _(
        "Please adjust your number of codes. Per module you can "
        "generate up to {} codes."
    )
    permission_required = "is_superuser"
    template_name = "meinberlin_votes/token_generation_dashboard.html"

    def get_permission_object(self):
        return self.project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["number_of_module_tokens"] = intcomma(
            TokenPackage.get_sum_token(self.module)
        )
        context["tokens_per_module"] = intcomma(TOKENS_PER_MODULE)
        return context

    def get_success_url(self):
        return reverse(
            "a4dashboard:voting-token-generation",
            kwargs={"module_slug": self.module.slug},
        )

    def form_valid(self, form):
        number_of_tokens = form.cleaned_data["number_of_tokens"]
        # check that no more than 5 Million codes are added per module
        existing_tokens = TokenPackage.get_sum_token(self.module)
        if existing_tokens + number_of_tokens > TOKENS_PER_MODULE:
            messages.error(
                self.request,
                self.error_message_token_number.format(intcomma(TOKENS_PER_MODULE)),
            )
        else:
            # make tasks to generate the tokens
            generate_voting_tokens(self.module.pk, number_of_tokens)

            messages.success(
                self.request,
                ngettext(
                    self.success_message[0], self.success_message[1], number_of_tokens
                ).format(intcomma(number_of_tokens)),
            )

        return redirect(self.get_success_url())
