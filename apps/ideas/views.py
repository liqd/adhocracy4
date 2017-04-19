import django_filters
from django.contrib import messages
from django.utils.translation import ugettext as _

from adhocracy4.modules import views as module_views

from apps.contrib import filters

from . import forms
from . import models


def get_ordering_choices(request):
    choices = (('-created', _('Most recent')),)
    if request.module.has_feature('rate', models.Idea):
        choices += ('-positive_rating_count', _('Most popular')),
    choices += ('-comment_count', _('Most commented')),
    return choices


class IdeaFilterSet(django_filters.FilterSet):

    category = filters.CategoryFilter()

    ordering = filters.OrderingFilter(
        choices=get_ordering_choices
    )

    class Meta:
        model = models.Idea
        fields = ['category']


class IdeaListView(module_views.ItemListView):
    model = models.Idea
    filter_set = IdeaFilterSet

    def get_queryset(self):
        return super().get_queryset().filter(module=self.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class IdeaDetailView(module_views.ItemDetailView):
    model = models.Idea
    queryset = models.Idea.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_ideas.view_idea'


class IdeaCreateView(module_views.ItemCreateView):
    model = models.Idea
    form_class = forms.IdeaForm
    permission_required = 'meinberlin_ideas.add_idea'
    template_name = 'meinberlin_ideas/idea_create_form.html'


class IdeaUpdateView(module_views.ItemUpdateView):
    model = models.Idea
    form_class = forms.IdeaForm
    permission_required = 'meinberlin_ideas.change_idea'
    template_name = 'meinberlin_ideas/idea_update_form.html'


class IdeaDeleteView(module_views.ItemDeleteView):
    model = models.Idea
    success_message = _("Your Idea has been deleted")
    permission_required = 'meinberlin_ideas.change_idea'
    template_name = 'meinberlin_ideas/idea_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(IdeaDeleteView, self).delete(request, *args, **kwargs)
