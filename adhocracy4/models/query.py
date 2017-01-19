from django.db import models


class RateableQuerySet(models.QuerySet):

    def _rate_value_condition(self, value):
        return models.Case(
            models.When(ratings__value=value, then=models.F('ratings__id')),
            output_field=models.IntegerField()
        )

    def annotate_positive_rating_count(self):
        return self.annotate(
            positive_rating_count=models.Count(
                self._rate_value_condition(1),
                distinct=True  # needed to combine with other count annotations
            )
        )

    def annotate_negative_rating_count(self):
        return self.annotate(
            negative_rating_count=models.Count(
                self._rate_value_condition(-1),
                distinct=True  # needed to combine with other count annotations
            )
        )


class CommentableQuerySet(models.QuerySet):

    def annotate_comment_count(self):
        return self.annotate(
            comment_count=models.Count(
                'comments',
                distinct=True  # needed to combine with other count annotations
            )
        )
