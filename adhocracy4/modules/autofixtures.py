from autofixture import AutoFixture, register

from .models import Module


class ModuleAutoFixture(AutoFixture):
    follow_pk = True

register(Module, ModuleAutoFixture)
