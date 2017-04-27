from django.forms import inlineformset_factory
from nested_formset import BaseNestedFormset
from nested_formset import BaseNestedModelForm


def nestedformset_factory(parent_model, model, nested_formset,
                          form=BaseNestedModelForm,
                          formset=BaseNestedFormset, fk_name=None,
                          fields=None, exclude=None, extra=3,
                          can_order=False, can_delete=True,
                          max_num=None, formfield_callback=None,
                          widgets=None, validate_max=False,
                          localized_fields=None, labels=None,
                          help_texts=None, error_messages=None,
                          min_num=None, validate_min=None):
    kwargs = {
        'form': form,
        'formfield_callback': formfield_callback,
        'formset': formset,
        'extra': extra,
        'can_delete': can_delete,
        'can_order': can_order,
        'fields': fields,
        'exclude': exclude,
        'min_num': min_num,
        'validate_min': validate_min,
        'max_num': max_num,
        'widgets': widgets,
        'validate_max': validate_max,
        'localized_fields': localized_fields,
        'labels': labels,
        'help_texts': help_texts,
        'error_messages': error_messages,
    }

    NestedFormSet = inlineformset_factory(
        parent_model,
        model,
        **kwargs
    )
    NestedFormSet.nested_formset_class = nested_formset

    return NestedFormSet
