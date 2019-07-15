from django import forms
from django.db.models import Max
from django.db.models import Min
from django.db.models import Q
from django.urls import resolve
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views import generic

RIGHT_OF_USE_LABEL = _('I hereby confirm that the copyrights for this '
                       'photo are with me or that I have received '
                       'rights of use from the author. I also confirm '
                       'that the privacy rights of depicted third persons '
                       'are not violated. ')


class DynamicChoicesMixin(object):
    """Dynamic choices mixin.

    Add callable functionality to filters that support the ``choices``
    argument. If the ``choices`` is callable, then it **must** accept the
    ``view`` object as a single argument.
    The ``view`` object may be None if the parent FilterSet is not class based.

    This is useful for dymanic ``choices`` determined properties on the
    ``view`` object.
    """

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super().__init__(*args, **kwargs)

    def get_choices(self, view):
        choices = self.choices

        if callable(choices):
            return choices(view)
        return choices

    @property
    def field(self):
        choices = self.get_choices(getattr(self, 'view', None))

        if choices is not None:
            self.extra['choices'] = choices

        return super(DynamicChoicesMixin, self).field


class ImageRightOfUseMixin(forms.ModelForm):
    right_of_use = forms.BooleanField(required=False, label=RIGHT_OF_USE_LABEL)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.image:
            self.initial['right_of_use'] = True

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        right_of_use = cleaned_data.get('right_of_use')
        if image and not right_of_use:
            self.add_error('right_of_use',
                           _("You want to upload an image. "
                             "Please check that you have the "
                             "right of use for the image."))


class ModuleClusterMixin:

    def _get_module_dict(self, count, start_date, end_date):
        return {
            'title': _('{}. Online Participation').format(str(count)),
            'type': 'module',
            'count': count,
            'date': start_date,
            'end_date': end_date,
            'modules': []
        }

    def get_module_clusters(self, modules):
        modules = modules\
            .exclude(Q(start_date=None) | Q(end_date=None))
        clusters = []
        try:
            start_date = modules.first().start_date
            end_date = modules.first().end_date
            count = 1
            first_cluster = self._get_module_dict(
                count, start_date, end_date)
            first_cluster['modules'].append(modules.first())
            current_cluster = first_cluster
            clusters.append(first_cluster)

            for module in modules[1:]:
                if module.start_date > end_date:
                    start_date = module.start_date
                    end_date = module.end_date
                    count += 1
                    next_cluster = self._get_module_dict(
                        count, start_date, end_date)
                    next_cluster['modules'].append(module)
                    current_cluster = next_cluster
                    clusters.append(next_cluster)
                else:
                    current_cluster['modules'].append(module)
                    if module.end_date > end_date:
                        end_date = module.end_date
                        current_cluster['end_date'] = end_date
        except AttributeError:
            return clusters
        if len(clusters) == 1:
            clusters[0]['title'] = _('Online Participation')
        return clusters


class DisplayProjectOrModuleMixin(generic.base.ContextMixin,
                                  ModuleClusterMixin):

    @cached_property
    def module_clusters(self):
        return super().get_module_clusters(self.modules)

    @cached_property
    def url_name(self):
        return resolve(self.request.path_info).url_name

    @cached_property
    def modules(self):
        return self.project.modules\
            .annotate(start_date=Min('phase__start_date'))\
            .annotate(end_date=Max('phase__end_date'))\
            .exclude(Q(start_date=None) | Q(end_date=None))\
            .order_by('start_date')

    @cached_property
    def events(self):
        return self.project.offlineevent_set.all()

    @cached_property
    def full_list(self):
        module_cluster = self.module_clusters
        event_list = self.get_events_list()
        full_list = module_cluster + list(event_list)
        return sorted(full_list, key=lambda k: k['date'])

    @cached_property
    def other_modules(self):
        for cluster in self.module_clusters(self.modules):
            if self.module in cluster['modules']:
                idx = cluster['modules'].index(self.module)
                modules = cluster['modules']
                return modules, idx
        return []

    @cached_property
    def extends(self):
        if self.url_name == 'module-detail':
            return 'a4modules/module_detail.html'
        return 'meinberlin_projects/project_detail.html'

    @cached_property
    def display_timeline(self):
        return len(self.full_list) > 1

    @cached_property
    def initial_slide(self):
        initial_slide = self.request.GET.get('initialSlide')
        if initial_slide:
            return int(initial_slide)
        else:
            now = timezone.now()
            for idx, val in enumerate(self.full_list):
                if 'type' in val and val['type'] == 'module':
                    start_date = val['date']
                    end_date = val['end_date']
                    if start_date and end_date:
                        if now >= start_date and now <= end_date:
                            return idx
        return 0

    def get_current_event(self):
        fl = self.full_list
        idx = self.initial_slide
        try:
            current_dict = fl[idx]
            if 'type' not in current_dict:
                return self.full_list[self.initial_slide]
        except (IndexError, KeyError):
            return []
        return []

    def get_current_modules(self):
        fl = self.full_list
        idx = self.initial_slide
        try:
            current_dict = fl[idx]
            if current_dict['type'] == 'module':
                return self.full_list[self.initial_slide]['modules']
        except (IndexError, KeyError):
            return []

    def get_events_list(self):
        return self.events.values('date', 'name',
                                  'event_type',
                                  'slug', 'description')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = self.url_name
        context['extends'] = self.extends
        if self.url_name == 'module-detail':
            cluster, idx = self.other_modules
            next_module = None
            previous_module = None
            try:
                next_module = cluster[idx + 1]
            except IndexError:
                pass
            try:
                previous_module = cluster[idx - 1]
            except IndexError:
                pass
            context['other_modules'] = cluster
            context['index'] = idx + 1
            context['next'] = next_module
            context['previous'] = previous_module
        else:
            context['event'] = self.get_current_event()
            context['modules'] = self.get_current_modules()
            context['participation_dates'] = self.full_list
            context['initial_slide'] = self.initial_slide
        return context
