from multiselectfield import MultiSelectField


class TopicField(MultiSelectField):
    """Deprecated, don't use"""

    # TODO: remove once topic migrations are rolled out
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 254
        kwargs["max_choices"] = 2
        kwargs["default"] = ""
        kwargs["blank"] = False
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        self.choices = ()

        # Call the super method at last so that choices are already initialized
        super().contribute_to_class(cls, name, **kwargs)
