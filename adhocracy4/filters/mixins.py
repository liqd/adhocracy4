class DynamicChoicesMixin(object):
    """Dynamic choices mixin.

    Add callable functionality to filters that support the ``choices``
    argument. If the ``choices`` is callable, then it **must** accept the
    ``view`` object as a single argument.
    The ``view`` object may be None if the parent FilterSet is not class based.

    This is useful for dymanic ``choices`` determined properties on the
    ``view`` object.
    """

    def __init__(self, *args, **kwargs):
        if "choices" in kwargs:
            self.choices = kwargs.pop("choices")
        super().__init__(*args, **kwargs)

    def get_choices(self, view):
        choices = self.choices

        if callable(choices):
            return choices(view)
        return choices

    @property
    def field(self):
        choices = self.get_choices(getattr(self, "view", None))

        if choices is not None:
            self.extra["choices"] = choices

        return super(DynamicChoicesMixin, self).field
