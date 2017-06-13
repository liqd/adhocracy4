# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

sql = """UPDATE django_content_type
         SET model = 'chapter'
         WHERE model = 'document' AND
               app_label = 'meinberlin_documents';"""

reverse_sql = """UPDATE django_content_type
                 SET model = 'document'
                 WHERE model = 'chapter' AND
                       app_label = 'meinberlin_documents';"""


class Migration(migrations.Migration):

    dependencies = [
        ('meinberlin_documents', '0004_remove_create_document_phase'),
    ]

    operations = [
        migrations.RunSQL(sql, reverse_sql)
    ]
