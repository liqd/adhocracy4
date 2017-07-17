from django.utils.translation import ugettext_lazy as _

from adhocracy4.filters import filters as a4_filters
from apps.contrib import filters
from apps.exports import views as export_views
from apps.ideas import views as idea_views

from . import forms
from . import models


def get_ordering_choices(request):
    choices = (('-created', _('Most recent')),)
    if request.project.last_active_module.has_feature('rate', models.MapIdea):
        choices += ('-positive_rating_count', _('Most popular')),
    choices += ('-comment_count', _('Most commented')),
    return choices


class MapIdeaFilterSet(a4_filters.DefaultsFilterSet):
    defaults = {
        'ordering': '-created'
    }
    category = filters.CategoryFilter()
    ordering = filters.OrderingFilter(
        choices=get_ordering_choices
    )

    class Meta:
        model = models.MapIdea
        fields = ['category']


class MapIdeaExportView(export_views.ItemExportView,
                        export_views.ItemExportWithRatesMixin,
                        export_views.ItemExportWithCommentCountMixin,
                        export_views.ItemExportWithCommentsMixin,
                        export_views.ItemExportWithLocationMixin):
    model = models.MapIdea
    fields = ['name', 'description', 'creator', 'created']

    def get_queryset(self):
        return super().get_queryset() \
            .filter(module=self.module)\
            .annotate_comment_count()\
            .annotate_positive_rating_count()\
            .annotate_negative_rating_count()


class MapIdeaListView(idea_views.AbstractIdeaListView):
    model = models.MapIdea
    filter_set = MapIdeaFilterSet
    exports = [(_('Ideas with location and comments'), MapIdeaExportView)]

    def dispatch(self, request, **kwargs):
        self.mode = request.GET.get('mode', 'map')
        if self.mode == 'map':
            self.paginate_by = 0
        return super().dispatch(request, **kwargs)

    def get_queryset(self):
        return super().get_queryset()\
            .filter(module=self.project.last_active_module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()


class MapIdeaDetailView(idea_views.AbstractIdeaDetailView):
    model = models.MapIdea
    queryset = models.MapIdea.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_mapideas.view_mapidea'


class MapIdeaCreateView(idea_views.AbstractIdeaCreateView):
    model = models.MapIdea
    form_class = forms.MapIdeaForm
    permission_required = 'meinberlin_mapideas.add_mapidea'
    template_name = 'meinberlin_mapideas/mapidea_create_form.html'


class MapIdeaUpdateView(idea_views.AbstractIdeaUpdateView):
    model = models.MapIdea
    form_class = forms.MapIdeaForm
    permission_required = 'meinberlin_mapideas.change_mapidea'
    template_name = 'meinberlin_mapideas/mapidea_update_form.html'


class MapIdeaDeleteView(idea_views.AbstractIdeaDeleteView):
    model = models.MapIdea
    success_message = _('Your Idea has been deleted')
    permission_required = 'meinberlin_mapideas.change_mapidea'
    template_name = 'meinberlin_mapideas/mapidea_confirm_delete.html'
