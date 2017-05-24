# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(help_text='Required. 60 characters or fewer. Letters, digits, spaces and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w]+[ \\w.@+-]*$', 'Enter a valid username. This value may contain only letters, digits, spaces and @/./+/-/_ characters. It must start with a digit or a letter.', 'invalid')], verbose_name='username', error_messages={'unique': 'A user with that username already exists.'}, max_length=60, unique=True)),
                ('email', models.EmailField(verbose_name='Email address', error_messages={'unique': 'A user with that email address already exists.'}, max_length=254, unique=True)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', blank=True, related_name='user_set', verbose_name='groups', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', to='auth.Permission', blank=True, related_name='user_set', verbose_name='user permissions', related_query_name='user')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
