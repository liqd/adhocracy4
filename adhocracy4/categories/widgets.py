from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms import widgets


class SelectWithIconWidget(widgets.Select):
    template_name = 'a4categories/widgets/select_icon.html'

    def create_option(self, name, value, label, selected, index, **kwargs):
        option = super().create_option(name, value, label, selected, index,
                                       **kwargs)

        icon_name = value if value else 'default'
        option['attrs']['data-icon-src'] = \
            static('category_icons/icons/{}_icon.svg'.format(icon_name))

        return option
