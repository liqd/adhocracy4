# fmt: off

from django.db import models
from django.utils.translation import gettext_lazy as _


class TopicEnum(models.TextChoices):
    """Choices for project topics."""

    ANT = "ANT", _("Anti-discrimination"),
    WOR = "WOR", _("Work & economy"),
    BUI = "BUI", _("Building & living"),
    EDU = "EDU", _("Education & research"),
    CHI = "CHI", _("Children, youth & family"),
    FIN = "FIN", _("Finances"),
    HEA = "HEA", _("Health & sports"),
    INT = "INT", _("Integration"),
    CUL = "CUL", _("Culture & leisure"),
    NEI = "NEI", _("Neighborhood & participation"),
    URB = "URB", _("Urban development"),
    ENV = "ENV", _("Environment & public green space"),
    TRA = "TRA", _("Traffic")
