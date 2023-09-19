from django_ckeditor_5.fields import CKEditor5Field

from adhocracy4.models.base import UserGeneratedContentModel


class ModeratorFeedback(UserGeneratedContentModel):
    feedback_text = CKEditor5Field(
        blank=True,
    )
