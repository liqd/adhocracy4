from collections import abc

from django import forms
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms import inlineformset_factory, widgets
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from adhocracy4.categories import models as category_models
from adhocracy4.dashboard.components.forms import ModuleDashboardFormSet
from adhocracy4.modules import models as module_models


def has_icons(module):
    if not hasattr(settings, 'A4_CATEGORY_ICONS'):
        return False

    module_settings = module.settings_instance
    return module_settings and hasattr(module_settings, 'polygon')


class CategorizableFieldMixin:
    category_field_name = 'category'

    def __init__(self, *args, **kwargs):
        module = kwargs.pop('module')
        super().__init__(*args, **kwargs)

        field = self.fields[self.category_field_name]
        field.queryset = category_models.Category.objects.filter(module=module)

        required = field.queryset.exists()
        field.empty_label = None
        field.required = required
        field.widget.is_required = required

    def show_categories(self):
        field = self.fields[self.category_field_name]
        module_has_categories = field.queryset.exists()
        return module_has_categories


class CategorySelectWidget(widgets.Select):
    def create_option(self, name, value, label, selected, index, **kwargs):
        option = super().create_option(name, value, label, selected, index,
                                       **kwargs)
        if value and value in self.icons:
            icon_name = self.icons[value]
            option['attrs']['data-icon-src'] = \
                static('category_icons/icons/{}_icon.svg'.format(icon_name))

        return option


class CategoryIconDict(abc.Mapping):
    def __init__(self, field):
        self.field = field
        self.queryset = field.queryset

    @cached_property
    def _icons(self):
        return {
            self.field.prepare_value(obj): getattr(obj, 'icon', None)
            for obj in self.queryset.all()
        }

    def __getitem__(self, key):
        return self._icons.__getitem__(key)

    def __iter__(self):
        return self._icons.__iter__()

    def __len__(self):
        return self._icons.__len__()


class CategoryChoiceField(forms.ModelChoiceField):
    widget = CategorySelectWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.icons = self.icons

    @property
    def icons(self):
        return CategoryIconDict(self)

    # Update the icons if the queryset is updated
    def _set_queryset(self, queryset):
        super()._set_queryset(queryset)
        self.widget.icons = self.icons

    queryset = property(forms.ModelChoiceField._get_queryset, _set_queryset)


class IconSelectWidget(widgets.Select):
    def create_option(self, name, value, label, selected, index, **kwargs):
        option = super().create_option(name, value, label, selected, index,
                                       **kwargs)

        icon_name = value if value else 'default'
        option['attrs']['data-icon-src'] = \
            static('category_icons/icons/{}_icon.svg'.format(icon_name))

        return option


class IconChoiceField(forms.TypedChoiceField):
    widget = IconSelectWidget


class CategoryForm(forms.ModelForm):
    def __init__(self, module, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Category name')
        self.fields['icon'].label = _('Category icon')

        if not (module and has_icons(module)):
            del self.fields['icon']

    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': _('Category')}
    ))

    class Media:
        js = ('js/category_formset.js',)

    class Meta:
        model = category_models.Category
        fields = ['name', 'icon']


class CategoryModuleDashboardFormSet(ModuleDashboardFormSet):
    def get_form_kwargs(self, index):
        form_kwargs = super().get_form_kwargs(index)
        form_kwargs['module'] = self.instance
        return form_kwargs


CategoryFormSet = inlineformset_factory(module_models.Module,
                                        category_models.Category,
                                        form=CategoryForm,
                                        formset=CategoryModuleDashboardFormSet,
                                        extra=0,
                                        )
