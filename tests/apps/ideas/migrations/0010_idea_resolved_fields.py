from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("a4test_ideas", "0009_idea_is_reviewed"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE a4test_ideas_idea ADD COLUMN "
                    "is_resolved boolean NOT NULL DEFAULT FALSE;",
                    reverse_sql="ALTER TABLE a4test_ideas_idea DROP COLUMN is_resolved;",
                ),
                migrations.RunSQL(
                    "ALTER TABLE a4test_ideas_idea ADD COLUMN "
                    "resolved_at timestamp with time zone NULL;",
                    reverse_sql="ALTER TABLE a4test_ideas_idea DROP COLUMN resolved_at;",
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="idea",
                    name="is_resolved",
                    field=models.BooleanField(default=False),
                ),
                migrations.AddField(
                    model_name="idea",
                    name="resolved_at",
                    field=models.DateTimeField(blank=True, null=True),
                ),
            ],
        ),
    ]
