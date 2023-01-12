from django.conf import settings
from django.db.models import CharField


class BlueprintTypeField(CharField):
    def contribute_to_class(self, cls, name, **kwargs):
        """Initialize the choices from the module's settings if they exist."""
        self.choices = getattr(settings, "A4_BLUEPRINT_TYPES", [])
        # Call the super method at last so that choices are already initialized
        super().contribute_to_class(cls, name, **kwargs)
