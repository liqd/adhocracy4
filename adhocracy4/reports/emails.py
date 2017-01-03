from django.contrib.auth import get_user_model
from django.contrib.sites import shortcuts
from django.core import urlresolvers

from euth.contrib import emails

User = get_user_model()


def send_email_to_moderators(request, report):
    obj = report.content_object
    name = obj._meta.verbose_name

    try:
        view = 'admin:{m.app_label}_{m.model_name}_change'.format(
            m=obj._meta)
        url = urlresolvers.reverse(view, args=(obj.pk,))
    except urlresolvers.NoReverseMatch:
        url = urlresolvers.reverse('admin:index')
    admin_url = request.build_absolute_uri(url)

    moderators = User.objects.filter(is_superuser=True)\
                             .values_list('email', flat=True)
    context = {
        'site': shortcuts.get_current_site(request),
        'name': name,
        'admin_url': admin_url,
        'description': report.description
    }

    emails.send_email_with_template(
        moderators, 'report_moderators', context
    )


def send_email_to_creator(request, report):
    obj = report.content_object
    receiver = obj.creator.email
    name = obj._meta.verbose_name

    context = {
        'site': shortcuts.get_current_site(request),
        'name': name,
        'description': report.description
    }

    emails.send_email_with_template([receiver], 'report_creator', context)
