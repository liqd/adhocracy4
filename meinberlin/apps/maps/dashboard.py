from adhocracy4.dashboard import components
from adhocracy4.dashboard.dashboard import ModuleAreaSettingsComponent
from adhocracy4.dashboard.forms import AreaSettingsForm

from .widgets import MapChoosePolygonWithPresetWidget


class ExtendedAreaSettingsForm(AreaSettingsForm):
    class Meta(AreaSettingsForm.Meta):
        widgets = {'polygon': MapChoosePolygonWithPresetWidget}


class ModuleExtendedAreaSettingsComponent(ModuleAreaSettingsComponent):
    form_class = ExtendedAreaSettingsForm


components.replace_module(ModuleExtendedAreaSettingsComponent())
