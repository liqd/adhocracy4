from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic

from adhocracy4.categories import filters as category_filters
from adhocracy4.categories import forms as category_forms
from adhocracy4.categories import models as category_models
from adhocracy4.dashboard import mixins as a4dashboard_mixins
from adhocracy4.exports.views import DashboardExportView
from adhocracy4.filters import filters as a4_filters
from adhocracy4.filters import views as filter_views
from adhocracy4.filters import widgets as filters_widgets
from adhocracy4.filters.filters import FreeTextFilter
from adhocracy4.labels import filters as label_filters
from adhocracy4.labels import forms as label_forms
from adhocracy4.labels import models as label_models
from adhocracy4.projects.mixins import DisplayProjectOrModuleMixin
from adhocracy4.projects.mixins import ProjectMixin
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib import forms as contrib_forms
from meinberlin.apps.contrib.views import CanonicalURLDetailView
from meinberlin.apps.moderatorfeedback.forms import ModeratorFeedbackForm
from meinberlin.apps.moderatorfeedback.models import ModeratorFeedback
from meinberlin.apps.moderatorremark.models import ModeratorRemark
from meinberlin.apps.notifications.emails import (
    NotifyCreatorOrContactOnModeratorFeedback,
)

from . import forms
from . import models


class FreeTextFilterWidget(filters_widgets.FreeTextFilterWidget):
    label = _("Search")


def get_ordering_choices(view):
    choices = (("-created", _("Most recent")),)
    if view.module.has_feature("rate", models.Idea):
        choices += (("-positive_rating_count", _("Most popular")),)
    choices += (("-comment_count", _("Most commented")),)
    return choices


class IdeaFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {"ordering": "-created"}
    ordering = a4_filters.DynamicChoicesOrderingFilter(choices=get_ordering_choices)
    search = FreeTextFilter(widget=FreeTextFilterWidget, fields=["name"])

    class Meta:
        model = models.Idea
        fields = ["search", "category", "labels"]

    def __init__(self, data, *args, **kwargs):
        self.base_filters["category"] = category_filters.CategoryAliasFilter(
            module=kwargs["view"].module, field_name="category"
        )
        self.base_filters["labels"] = label_filters.LabelAliasFilter(
            module=kwargs["view"].module, field_name="labels"
        )
        super().__init__(data, *args, **kwargs)


class AbstractIdeaListView(ProjectMixin, filter_views.FilteredListView):
    paginate_by = 15

    def get_queryset(self):
        """Annotations normally happen in the filters, but if e.g. filtering is called with an invalid
        value, it doesn't get there, this is why we need to check here again.
        Also, token vote annotation only happens here as we did not add it to the django filters (we only
        use them in the api).
        """
        qs = super().get_queryset().filter(module=self.module)
        if qs:
            if not hasattr(qs.first(), "comment_count"):
                qs = qs.annotate_comment_count()
            if hasattr(qs, "annotate_positive_rating_count") and not hasattr(
                qs.first(), "positive_rating_count"
            ):
                qs = (
                    qs.annotate_positive_rating_count().annotate_negative_rating_count()
                )
            if hasattr(qs, "annotate_token_vote_count") and not hasattr(
                qs.first(), "token_vote_count"
            ):
                qs = qs.annotate_token_vote_count()
        return qs


class IdeaListView(AbstractIdeaListView, DisplayProjectOrModuleMixin):
    model = models.Idea
    filter_set = IdeaFilterSet

    def get_queryset(self):
        return super().get_queryset().filter(module=self.module)


class AbstractIdeaDetailView(
    ProjectMixin, rules_mixins.PermissionRequiredMixin, CanonicalURLDetailView
):
    get_context_from_object = True


class IdeaDetailView(AbstractIdeaDetailView):
    model = models.Idea
    queryset = (
        models.Idea.objects.annotate_positive_rating_count().annotate_negative_rating_count()
    )
    permission_required = "meinberlin_ideas.view_idea"


class AbstractIdeaCreateView(
    ProjectMixin, rules_mixins.PermissionRequiredMixin, generic.CreateView
):
    """Create an idea in the context of a module."""

    def get_permission_object(self, *args, **kwargs):
        return self.module

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.module = self.module
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["module"] = self.module
        if self.module.settings_instance:
            kwargs["settings_instance"] = self.module.settings_instance
        return kwargs


class IdeaCreateView(AbstractIdeaCreateView):
    model = models.Idea
    form_class = forms.IdeaForm
    permission_required = "meinberlin_ideas.add_idea"
    template_name = "meinberlin_ideas/idea_create_form.html"


class AbstractIdeaUpdateView(
    ProjectMixin, rules_mixins.PermissionRequiredMixin, generic.UpdateView
):
    get_context_from_object = True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = kwargs.get("instance")
        kwargs["module"] = instance.module
        if instance.module.settings_instance:
            kwargs["settings_instance"] = instance.module.settings_instance
        return kwargs


class IdeaUpdateView(AbstractIdeaUpdateView):
    model = models.Idea
    form_class = forms.IdeaForm
    permission_required = "meinberlin_ideas.change_idea"
    template_name = "meinberlin_ideas/idea_update_form.html"


class AbstractIdeaDeleteView(
    ProjectMixin, rules_mixins.PermissionRequiredMixin, generic.DeleteView
):
    get_context_from_object = True

    def get_success_url(self):
        return reverse("project-detail", kwargs={"slug": self.project.slug})

    def form_valid(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().form_valid(request, *args, **kwargs)


class IdeaDeleteView(AbstractIdeaDeleteView):
    model = models.Idea
    success_message = _("Your Idea has been deleted")
    permission_required = "meinberlin_ideas.change_idea"
    template_name = "meinberlin_ideas/idea_confirm_delete.html"


class AbstractIdeaModerateView(
    ProjectMixin,
    rules_mixins.PermissionRequiredMixin,
    generic.detail.SingleObjectMixin,
    generic.detail.SingleObjectTemplateResponseMixin,
    contrib_forms.BaseMultiModelFormView,
):
    get_context_from_object = True
    remark_form_class = None

    def __init__(self):
        self.forms = {
            "moderateable": {
                "model": self.model,
                "form_class": self.moderateable_form_class,
            },
            "feedback_text": {
                "model": ModeratorFeedback,
                "form_class": ModeratorFeedbackForm,
            },
        }
        # FIXME: use the form class directly here and remove "if"-condition
        # when used for all ideas and not only for budgeting proposals
        if self.remark_form_class:
            self.forms["remark"] = {
                "model": ModeratorRemark,
                "form_class": self.remark_form_class,
            }

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def forms_save(self, forms, commit=True):
        objects = super().forms_save(forms, commit=False)
        moderateable = objects["moderateable"]
        feedback_text = objects["feedback_text"]
        # FIXME: use the remark directly and remove "if"-condition
        # when used for all ideas and not only for budgeting proposals
        remark = None
        if "remark" in objects:
            remark = objects["remark"]
            if not remark.pk:
                remark.creator = self.request.user

        if not feedback_text.pk:
            feedback_text.creator = self.request.user

        with transaction.atomic():
            feedback_text.save()
            moderateable.moderator_feedback_text = feedback_text
            moderateable.save()
            # FIXME: remove "if"-condition when form used for all ideas
            if remark:
                remark.item = moderateable
                remark.save()

            if (
                "moderator_status" in forms["moderateable"].changed_data
                or "feedback_text" in forms["feedback_text"].changed_data
            ):
                NotifyCreatorOrContactOnModeratorFeedback.send(self.object)
        return objects

    def get_instance(self, name):
        if name == "moderateable":
            return self.object
        elif name == "feedback_text":
            return self.object.moderator_feedback_text
        elif name == "remark":
            return self.object.remark


class IdeaModerateView(AbstractIdeaModerateView):
    model = models.Idea
    permission_required = "meinberlin_ideas.moderate_idea"
    template_name = "meinberlin_ideas/idea_moderate_form.html"
    moderateable_form_class = forms.IdeaModerateForm


class IdeaDashboardExportView(DashboardExportView):
    template_name = "a4exports/export_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["export"] = reverse(
            "a4dashboard:idea-export", kwargs={"module_slug": self.module.slug}
        )
        context["comment_export"] = reverse(
            "a4dashboard:idea-comment-export", kwargs={"module_slug": self.module.slug}
        )
        return context


class DashboardCategoriesWithAliasView(
    ProjectMixin,
    a4dashboard_mixins.DashboardBaseMixin,
    a4dashboard_mixins.DashboardComponentMixin,
    generic.UpdateView,
):
    model = category_models.CategoryAlias
    template_name = "a4categories/includes/module_categories_form.html"
    form_class = category_forms.CategoryAliasForm
    permission_required = "a4projects.change_project"

    def get_permission_object(self):
        return self.project

    def get_object(self):
        return category_models.CategoryAlias.objects.filter(module=self.module).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = category_forms.CategoryFormSet(
                self.request.POST, instance=self.module
            )
        else:
            context["formset"] = category_forms.CategoryFormSet(instance=self.module)
        context["category_form"] = category_forms.CategoryForm(module=self.module)
        return context

    def form_valid(self, form):
        form.instance.module = self.module
        context = self.get_context_data()
        formset = context["formset"]
        with transaction.atomic():
            if formset.is_valid():
                formset.instance = self.module
                formset.save()
        return super().form_valid(form)


class DashboardLabelsWithAliasView(
    ProjectMixin,
    a4dashboard_mixins.DashboardBaseMixin,
    a4dashboard_mixins.DashboardComponentMixin,
    generic.UpdateView,
):
    model = label_models.LabelAlias
    template_name = "a4labels/includes/module_labels_form.html"
    form_class = label_forms.LabelAliasForm
    permission_required = "a4projects.change_project"

    def get_permission_object(self):
        return self.project

    def get_object(self):
        return label_models.LabelAlias.objects.filter(module=self.module).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = label_forms.LabelsFormSet(
                self.request.POST, instance=self.module
            )
        else:
            context["formset"] = label_forms.LabelsFormSet(instance=self.module)
        context["label_form"] = label_forms.LabelForm(module=self.module)
        return context

    def form_valid(self, form):
        form.instance.module = self.module
        context = self.get_context_data()
        formset = context["formset"]
        with transaction.atomic():
            if formset.is_valid():
                formset.instance = self.module
                formset.save()
        return super().form_valid(form)
