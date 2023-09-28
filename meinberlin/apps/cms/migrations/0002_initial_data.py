# -*- coding: utf-8 -*-
from django.db import migrations


def create_initial_data(apps, schema_editor):
    # Get models
    ContentType = apps.get_model("contenttypes.ContentType")
    Page = apps.get_model("wagtailcore.Page")
    Site = apps.get_model("wagtailcore.Site")
    HomePage = apps.get_model("meinberlin_cms.HomePage")
    NavigationMenu = apps.get_model("meinberlin_cms.NavigationMenu")

    # Delete the default homepage
    Page.objects.get(id=2).delete()

    # Create content type for homepage model
    homepage_content_type, created = ContentType.objects.get_or_create(
        model="homepage", app_label="meinberlin_cms"
    )

    # Create a new homepage
    homepage = HomePage.objects.create(
        title="Homepage",
        slug="home",
        content_type=homepage_content_type,
        path="00010001",
        depth=2,
        numchild=0,
        url_path="/home/",
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(hostname="localhost", root_page=homepage, is_default_site=True)

    # create top navigation snippet
    NavigationMenu.objects.create(title="topnav")


class Migration(migrations.Migration):
    run_before = [
        ("wagtailcore", "0053_locale_model"),  # added for Wagtail 2.11 compatibility
    ]

    dependencies = [
        ("wagtailcore", "0002_initial_data"),
        ("meinberlin_cms", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
