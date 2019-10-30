from autofixture import AutoFixture
from autofixture import register

from .models import Module


class ModuleAutoFixture(AutoFixture):
    follow_pk = True


register(Module, ModuleAutoFixture)
