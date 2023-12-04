from django.conf import settings
from django.db import migrations

from adhocracy4.dashboard.blueprints import get_blueprints
from meinberlin.apps.bplan.views import BplanProjectCreateView
from meinberlin.apps.extprojects.views import ExternalProjectCreateView


def determine_and_add_blueprint_types_to_modules(apps, schema_editor):
    """Determine the blueprint type of existing modules by their phase set
    and add accordingly.

    Run this migration after types have been added to blueprints and
    'A4_BLUEPRINT_TYPES have been added to settings.'
    """
    if hasattr(settings, "A4_BLUEPRINT_TYPES"):
        blueprints = [blueprint[1] for blueprint in get_blueprints()]
        blueprints.append(BplanProjectCreateView.blueprint)
        blueprints.append(ExternalProjectCreateView.blueprint)

        # create dictionary with concatenated phase identifiers as keys
        # and type as values
        phase_identifiers_to_blueprint_type = {
            "-".join([phase.identifier for phase in blueprint.content]): blueprint.type
            for blueprint in blueprints
        }

        Module = apps.get_model("a4modules", "Module")
        for module in Module.objects.all():
            phase_identifiers_str = "-".join(
                [phase.type for phase in module.phase_set.all()]
            )
            if (
                phase_identifiers_str in phase_identifiers_to_blueprint_type
                and not module.blueprint_type
            ):
                module.blueprint_type = phase_identifiers_to_blueprint_type[
                    phase_identifiers_str
                ]
                module.save()


def remove_blueprint_types(apps, schema_editor):
    Module = apps.get_model("a4modules", "Module")
    for module in Module.objects.all():
        module.blueprint_type = ""
        module.save()


class Migration(migrations.Migration):
    dependencies = [
        ("meinberlin_projects", "0002_custom_project_types"),
        ("a4modules", "0006_module_blueprint_type"),
    ]

    operations = [
        migrations.RunPython(
            determine_and_add_blueprint_types_to_modules, remove_blueprint_types
        ),
    ]
