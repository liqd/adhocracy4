# Generated by Django 3.2.20 on 2023-11-16 11:35

from bs4 import BeautifulSoup
from django.db import migrations


def replace_iframe_with_figur(apps, schema_editor):
    template = (
        '<figure class="media"><div data-oembed-url="{url}"><div><iframe src="'
        '{url}"></iframe></div></div></figure>'
    )
    Project = apps.get_model("a4projects", "Project")
    informations = 0
    results = 0
    for project in Project.objects.all():
        soup = BeautifulSoup(project.information, "html.parser")
        iframes = soup.findAll("iframe")
        changed = False
        for iframe in iframes:
            figure = BeautifulSoup(
                template.format(url=iframe.attrs["src"]), "html.parser"
            )
            iframe.replaceWith(figure)
            informations += 1
        if iframes:
            project.information = soup.prettify(formatter="html")
            changed = True
        soup = BeautifulSoup(project.result, "html.parser")
        iframes = soup.findAll("iframe")
        for iframe in iframes:
            figure = BeautifulSoup(
                template.format(url=iframe.attrs["src"]), "html.parser"
            )
            iframe.replaceWith(figure)
            results += 1
        if iframes:
            project.result = soup.prettify(formatter="html")
            changed = True
        if changed:
            project.save()


class Migration(migrations.Migration):
    dependencies = [
        ("a4projects", "0040_auto_20230919_0952"),
    ]

    operations = [
        migrations.RunPython(
            replace_iframe_with_figur,
        ),
    ]
