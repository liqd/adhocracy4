import django_filters
from django.contrib import messages
from django.utils.translation import ugettext as _

from adhocracy4.maps import mixins as map_mixins
from adhocracy4.modules import views as module_views

from apps.contrib import filters

from . import forms
from . import models


def get_ordering_choices(request):
    choices = (('-created', _('Most recent')),)
    if request.module.has_feature('rate', models.MapIdea):
        choices += ('-positive_rating_count', _('Most popular')),
    choices += ('-comment_count', _('Most commented')),
    return choices


class MapIdeaFilterSet(django_filters.FilterSet):

    category = filters.CategoryFilter()

    ordering = filters.OrderingFilter(
        choices=get_ordering_choices
    )

    @property
    def qs(self):
        return super().qs.filter(module=self.request.module) \
            .annotate_positive_rating_count() \
            .annotate_negative_rating_count() \
            .annotate_comment_count()

    class Meta:
        model = models.MapIdea
        fields = ['category']


class MapIdeaListView(map_mixins.MapItemListMixin, module_views.ItemListView):
    model = models.MapIdea
    filter_set = MapIdeaFilterSet


class MapIdeaDetailView(map_mixins.MapItemDetailMixin,
                        module_views.ItemDetailView):
    model = models.MapIdea
    queryset = models.MapIdea.objects.annotate_positive_rating_count()\
        .annotate_negative_rating_count()
    permission_required = 'meinberlin_mapideas.view_idea'


class MapIdeaCreateView(module_views.ItemCreateView):
    model = models.MapIdea
    form_class = forms.MapIdeaForm
    permission_required = 'meinberlin_mapideas.create_idea'
    template_name = 'meinberlin_mapideas/mapidea_create_form.html'


class MapIdeaUpdateView(module_views.ItemUpdateView):
    model = models.MapIdea
    form_class = forms.MapIdeaForm
    permission_required = 'meinberlin_mapideas.change_idea'
    template_name = 'meinberlin_mapideas/mapidea_update_form.html'


class MapIdeaDeleteView(module_views.ItemDeleteView):
    model = models.MapIdea
    success_message = _("Your Idea has been deleted")
    permission_required = 'meinberlin_mapideas.change_idea'
    template_name = 'meinberlin_mapideas/mapidea_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)
