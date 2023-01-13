from django.db import models

from meinberlin.apps.livequestions.models import LiveQuestion


class Like(models.Model):
    session = models.CharField(max_length=255)
    question = models.ForeignKey(
        LiveQuestion, related_name="question_likes", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "question")
