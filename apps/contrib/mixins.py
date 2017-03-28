class ChoicesRequestMixin(object):
    """Dynamic choices mixin.

    Add callable functionality to filters that support the ``choices``
    argument. If the ``choices`` is callable, then it **must** accept the
    ``request`` object as a single argument.

    This is useful for dymanic ``choices`` determined properties on the
    ``request`` object.
    """

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices')
        super().__init__(*args, **kwargs)

    def get_request(self):
        try:
            return self.parent.request
        except AttributeError:
            return None

    def get_choices(self, request):
        choices = self.choices

        if callable(choices):
            return choices(request)
        return choices

    @property
    def field(self):
        request = self.get_request()
        choices = self.get_choices(request)

        if choices is not None:
            self.extra['choices'] = choices

        return super(ChoicesRequestMixin, self).field
