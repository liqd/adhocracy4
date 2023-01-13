# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db import models

import adhocracy4.images.fields


class Migration(migrations.Migration):

    dependencies = [
        ("meinberlin_organisations", "0003_logo-for-newsletter"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organisation",
            name="logo",
            field=adhocracy4.images.fields.ConfiguredImageField(
                "logo",
                upload_to="organisation/logos",
                help_prefix="The image will be shown in the newsletter in the banner.",
                blank=True,
                verbose_name="Logo",
            ),
        ),
    ]
