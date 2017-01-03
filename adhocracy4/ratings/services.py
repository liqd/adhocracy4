from . import models


def delete_ratings(contenttype, pk):
    ratings = models.Rating.objects.all().filter(
        content_type=contenttype, object_pk=pk)
    for rating in ratings:
        rating.delete()
