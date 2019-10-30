from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from adhocracy4.dashboard import ModuleFormSetComponent
from adhocracy4.dashboard import components

from . import forms


class ModuleCategoriesComponent(ModuleFormSetComponent):
    identifier = 'categories'
    weight = 13
    label = _('Categories')

    form_title = _('Edit categories')
    form_class = forms.CategoryFormSet
    form_template_name = 'a4categories/includes/module_categories_form.html'

    def is_effective(self, module):
        module_app = module.phases[0].content().app
        for app, name in settings.A4_CATEGORIZABLE:
            if app == module_app:
                return True
        return False


components.register_module(ModuleCategoriesComponent())
