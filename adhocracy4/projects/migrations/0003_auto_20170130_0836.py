# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('a4projects', '0002_change_to_configured_image_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='moderators',
            field=models.ManyToManyField(blank=True, related_name='project_moderator', to=settings.AUTH_USER_MODEL),
        ),
    ]
