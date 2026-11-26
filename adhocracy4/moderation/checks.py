from django.core import checks
from django.utils.translation import gettext_lazy as _

from . import utils


@checks.register()
def check_moderation_itemables(app_configs, **kwargs):
    errors = []
    for model in utils.get_item_models():
        field_names = {field.name for field in model._meta.get_fields()}
        for field_name in ("is_reviewed", "is_resolved"):
            if field_name not in field_names:
                errors.append(
                    checks.Error(
                        "Moderatable item model '{}' has no '{}' field.".format(
                            model._meta.label, field_name
                        ),
                        hint=_(
                            "Add the field or remove the model from "
                            "A4_MODERATION_ITEMABLES."
                        ),
                        id="a4moderation.E001",
                    )
                )
    return errors
