from autofixture import AutoFixture, generators, register
from django.contrib.contenttypes.models import ContentType

from home.models import HomePage

from .models import Comment


class CommentAutoFixture(AutoFixture):

    homepage_contenttype = ContentType.objects.get(app_label='home',
                                                   model='homepage')
    homepage_id = HomePage.objects.first().pk

    field_values = {
        'content_type': homepage_contenttype,
        'object_pk': homepage_id,
        'is_removed': generators.BooleanGenerator(),
        'is_censored': generators.BooleanGenerator(),
    }


register(Comment, CommentAutoFixture)
