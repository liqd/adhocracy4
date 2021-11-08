from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from adhocracy4.dashboard import DashboardComponent
from adhocracy4.dashboard import components

from . import exports
from . import models
from . import views


class MapTopicEditComponent(DashboardComponent):
    identifier = 'map_topic_edit'
    weight = 20
    label = _('Places')

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        if module_app != 'meinberlin_maptopicprio':
            return False
        elif module.settings_instance.polygon == '':
            return False
        else:
            return True

    def get_progress(self, module):
        if models.MapTopic.objects.filter(module=module).exists():
            return 1, 1
        return 0, 1

    def get_base_url(self, module):
        return reverse('a4dashboard:maptopic-list', kwargs={
            'module_slug': module.slug
        })

    def get_urls(self):
        return [
            (r'^maptopics/module/(?P<module_slug>[-\w_]+)/$',
             views.MapTopicListDashboardView.as_view(component=self),
             'maptopic-list'),
            (r'^maptopics/create/module/(?P<module_slug>[-\w_]+)/$',
             views.MapTopicCreateView.as_view(component=self),
             'maptopic-create'),
            (r'^maptopics/(?P<year>\d{4})-(?P<pk>\d+)/update/$',
             views.MapTopicUpdateView.as_view(component=self),
             'maptopic-update'),
            (r'^maptopics/(?P<year>\d{4})-(?P<pk>\d+)/delete/$',
             views.MapTopicDeleteView.as_view(component=self),
             'maptopic-delete')
        ]


components.register_module(MapTopicEditComponent())


class ExportMapTopicComponent(DashboardComponent):
    identifier = 'maptopic_export'
    weight = 50
    label = _('Export Excel')

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        return (module_app == 'meinberlin_maptopicprio' and
                not module.project.is_draft and not module.is_draft)

    def get_progress(self, module):
        return 0, 0

    def get_base_url(self, module):
        return reverse('a4dashboard:maptopic-export-module', kwargs={
            'module_slug': module.slug,
        })

    def get_urls(self):
        return [
            (r'^modules/(?P<module_slug>[-\w_]+)/export/maptopic/$',
             views.MapTopicDashboardExportView.as_view(),
             'maptopic-export-module'),
            (r'^modules/(?P<module_slug>[-\w_]+)/export/maptopic/maptopics/$',
             exports.MapTopicExportView.as_view(),
             'maptopic-export'),
            (r'^modules/(?P<module_slug>[-\w_]+)/export/maptopic/comments/$',
             exports.MapTopicCommentExportView.as_view(),
             'maptopic-comment-export'),
        ]


components.register_module(ExportMapTopicComponent())
