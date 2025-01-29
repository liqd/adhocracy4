from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured
from django.forms.widgets import Widget
from django.template import loader


class MapChoosePointWidget(Widget):
    def __init__(self, polygon, attrs=None):
        self.polygon = polygon
        super().__init__(attrs)

    class Media:
        js = ("a4maps_react_choose_point.js",)

        css = {"all": ["a4maps_react_choose_point.css"]}

    def render(self, name, value, attrs, renderer=None):
        if not finders.find("a4maps_react_choose_point.js"):
            raise ImproperlyConfigured(
                "Configure your frontend build tool to generate a4maps_react_choose_point.js."
            )

        context = {
            "name": name,
            "polygon": self.polygon,
        }

        if value != "null" and value:
            context["point"] = value

        return loader.render_to_string(
            "a4maps_react/map_choose_point_widget.html", context
        )
