from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("a4test_ideas", "0008_alter_idea_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="idea",
            name="is_reviewed",
            field=models.BooleanField(default=False),
        ),
    ]
