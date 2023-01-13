from ckeditor.fields import RichTextField

from adhocracy4.models.base import UserGeneratedContentModel


class ModeratorFeedback(UserGeneratedContentModel):
    feedback_text = RichTextField(
        blank=True,
    )
