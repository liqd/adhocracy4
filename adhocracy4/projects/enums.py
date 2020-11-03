from enum import auto

from django.utils.translation import ugettext_lazy as _
from django_enumfield.enum import Enum


class Access(Enum):
    PUBLIC = auto()
    SEMIPUBLIC = auto()
    PRIVATE = auto()

    __labels__ = {
        PUBLIC: _("public"),
        SEMIPUBLIC: _("semipublic"),
        PRIVATE: _("private")
    }
