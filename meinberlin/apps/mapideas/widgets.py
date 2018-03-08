from django.contrib.staticfiles.templatetags.staticfiles import static

from adhocracy4.categories.widgets import SelectWithIconWidget


class SelectCategoryWithIconWidget(SelectWithIconWidget):

    def create_option(self, name, value, label, selected, index, **kwargs):
        option = super().create_option(name, value, label, selected, index,
                                       **kwargs)

        icon_name = (self.attrs['qs'][index].icon
                     if self.attrs['qs'][index].icon
                     else 'default')
        option['attrs']['data-icon-src'] = \
            static('category_icons/icons/{}_icon.svg'.format(icon_name))

        return option
