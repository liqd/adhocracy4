from enum import auto

from django.utils.translation import ugettext_lazy as _
from django_enumfield.enum import Enum


class Access(Enum):
    PRIVATE = auto()
    PUBLIC = auto()
    SEMIPUBLIC = auto()

    __labels__ = {
        PRIVATE: _("private"),
        PUBLIC: _("public"),
        SEMIPUBLIC: _("semipublic")
    }
