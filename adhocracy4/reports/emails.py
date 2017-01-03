from django.contrib.auth import get_user_model
from django.core import urlresolvers

from adhocracy4.emails import email

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
        'name': name,
        'admin_url': admin_url,
        'description': report.description
    }

    email.send_email_with_template(
        moderators, 'report_moderators', context
    )


def send_email_to_creator(report):
    obj = report.content_object
    receiver = obj.creator.email
    name = obj._meta.verbose_name

    context = {
        'name': name,
        'description': report.description
    }

    email.send_email_with_template([receiver], 'report_creator', context)
