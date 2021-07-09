from ckeditor.fields import RichTextField

from adhocracy4.models.base import UserGeneratedContentModel


class ModeratorStatement(UserGeneratedContentModel):
    statement = RichTextField(
        blank=True,
    )
