# flake8: noqa

from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.forms import models as model_forms
from django.forms.formsets import all_valid
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views import generic


class MultiFormMixin(generic.base.ContextMixin):
    forms = {}
    success_url = None
    prefix = None

    def forms_invalid(self, forms):
        """
        If any form is invalid, re-render the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(self.get_context_data(forms=forms))

    def forms_valid(self, forms):
        """
        If all forms are valid, redirect to the supplied URL.
        """
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """
        Insert the forms into the context dict.
        """
        if 'forms' not in kwargs:
            kwargs['forms'] = self.get_forms()
        return super().get_context_data(**kwargs)

    def get_forms(self):
        """
        Returns instances of the forms to be used in this view.
        """
        forms = {}
        for name in self.forms.keys():
            form_class = self.get_form_class(name)
            if form_class:
                forms[name] = form_class(**self.get_form_kwargs(name))
        return forms

    def _get_from_name(self, name, key, default=None):
        form = self.forms.get(name)
        if form:
            return form.get(key, default)

    def get_form_class(self, name):
        """
        Returns the form class to be used with the named form.
        """
        return self._get_from_name(name, 'form_class')

    def get_initial(self, name):
        """
        Returns the initial data to use for the named form.
        """
        initial = self._get_from_name(name, 'initial', {})
        return initial.copy()

    def get_prefix(self, name):
        """
        Returns the prefix to use for the named form.
        """
        if self.prefix:
            return '{}_{}'.format(self.prefix, name)
        return name

    def get_form_kwargs(self, name):
        """
        Returns the keyword arguments for instantiating the named form.
        """
        kwargs = {
            'initial': self.get_initial(name),
            'prefix': self.get_prefix(name),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url


class MultiModelFormMixin(MultiFormMixin):
    objects = {}

    def forms_valid(self, forms):
        """
        If all forms are valid, save the associated models.
        """
        self.objects = self.forms_save(forms)
        self.forms_save_m2m(forms)
        return super().forms_valid(forms)

    def forms_save(self, forms, commit=True):
        """
        Save all the forms in one transaction.
        """
        objects = {}
        with transaction.atomic():
            for name in self.forms.keys():
                if hasattr(forms[name], 'save'):
                    objects[name] = forms[name].save(commit)
        return objects

    def forms_save_m2m(self, forms):
        """
        Calls save_m2m on every form where it is available.
        Has to be called after the forms have been saved.
        """
        for form in forms.values():
            if hasattr(form, 'save_m2m'):
                form.save_m2m()

    def get_form_class(self, name):
        """
        Returns the form class to be used with the named form.
        """
        fields = self._get_from_name(name, 'fields')
        form_class = self._get_from_name(name, 'form_class')
        model = self._get_from_name(name, 'model')

        if fields is not None and form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )

        if form_class:
            return form_class
        elif model is not None:
            if fields is None:
                raise ImproperlyConfigured(
                    "Using MultiModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited."
                    % self.__class__.__name__
                )
            return model_forms.modelform_factory(model, fields=fields)

    def get_form_kwargs(self, name):
        """
        Returns the keyword arguments for instantiating the named form.
        """
        kwargs = super().get_form_kwargs(name)
        instance = self.get_instance(name)
        if instance:
            kwargs.update({'instance': instance})
        return kwargs

    def get_instance(self, name):
        """
        Returns the instance object used for instantiating the named form.
        If no instance (None) is returned the django BaseModelForm
        creates a default instance of the provided model.
        """
        pass


class ProcessMultiFormView(generic.View):
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        forms = self.get_forms()

        if all_valid(forms.values()):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)

    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseMultiFormView(MultiFormMixin, ProcessMultiFormView):
    """
    A base view for displaying multiple forms.
    """


class BaseMultiModelFormView(MultiModelFormMixin, ProcessMultiFormView):
    """
    A base view for displaying multiple forms that may contain ModelForms.
    """
