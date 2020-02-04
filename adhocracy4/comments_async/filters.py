from django.db import models
from rest_framework.filters import BaseFilterBackend
from rest_framework.filters import SearchFilter


class CommentCategoryFilterBackend(BaseFilterBackend):
    """Filter the comments for the categories."""

    def filter_queryset(self, request, queryset, view):

        if 'comment_category' in request.GET:
            category = request.GET['comment_category']
            return queryset.filter(comment_categories__contains=category)

        return queryset


class CommentOrderingFilterBackend(BaseFilterBackend):
    """Order the comments."""

    def filter_queryset(self, request, queryset, view):

        if 'ordering' in request.GET:
            ordering = request.GET['ordering']

            if ordering == 'new':
                return queryset.order_by('-created')
            elif ordering == 'ans':
                queryset = queryset\
                    .annotate(comment_count=models.Count(
                        'child_comments', distinct=True))
                return queryset.order_by('-comment_count', '-created')
            elif ordering == 'pos':
                queryset = queryset\
                    .annotate(positive_rating_count=models.Count(
                        models.Case(
                            models.When(
                                ratings__value=1,
                                then=models.F('ratings__id')
                            ),
                            output_field=models.IntegerField()
                        ),
                        distinct=True))
                return queryset.order_by('-positive_rating_count', '-created')
            elif ordering == 'neg':
                queryset = queryset\
                    .annotate(negative_rating_count=models.Count(
                        models.Case(
                            models.When(
                                ratings__value=-1,
                                then=models.F('ratings__id')
                            ),
                            output_field=models.IntegerField()
                        ),
                        distinct=True))
                return queryset.order_by('-negative_rating_count', '-created')
            elif ordering == 'dis':
                return queryset.order_by(
                    models.F('last_discussed').desc(nulls_last=True),
                    '-created'
                )
            elif ordering == 'mom':
                return queryset.order_by('-is_moderator_marked', '-created')

        return queryset


class CustomSearchFilter(SearchFilter):

    def filter_queryset(self, request, queryset, view):
        qs = super().filter_queryset(request, queryset, view)
        if self.get_search_terms(request):
            return qs.filter(is_removed=False, is_censored=False)
        return qs
