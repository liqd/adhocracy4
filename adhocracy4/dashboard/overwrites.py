from django.utils.translation import ugettext_lazy as _

from adhocracy4.projects.enums import Access


def overwrite_access_enum_label():
    Access.__labels__ = {
        Access.PRIVATE: _('Only invited users can see project tile and '
                          'content and can participate (private).'),
        Access.PUBLIC: _('All users can see project tile and content and can '
                         'participate (public).'),
        Access.SEMIPUBLIC: _('All users can see project tile and content, '
                             'only invited users can participate '
                             '(semi-public).')
    }
