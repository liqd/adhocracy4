from adhocracy4.test import factories

from . import models


class QuestionFactory(factories.ItemFactory):
    class Meta:
        model = models.Question
